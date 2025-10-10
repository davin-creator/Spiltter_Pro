import os
import pandas as pd
import zipfile
from io import BytesIO
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ---- Folders ----
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output_splits"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---- File Split Function ----
def split_file_by_column(file_path, column_name, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext in [".xlsx", ".xls"]:
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        unique_values = set()
        for df in all_sheets.values():
            if column_name in df.columns:
                unique_values.update(df[column_name].dropna().unique())

        for value in unique_values:
            safe_value = str(value).replace("/", "_").replace("\\", "_").replace(":", "_")
            output_file = os.path.join(output_folder, f"{safe_value}.xlsx")

            with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
                sheet_written = False
                for sheet_name, df in all_sheets.items():
                    if column_name not in df.columns:
                        continue
                    filtered_df = df[df[column_name] == value]
                    if not filtered_df.empty:
                        filtered_df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
                        sheet_written = True
            if not sheet_written and os.path.exists(output_file):
                os.remove(output_file)

    elif file_ext == ".csv":
        df = pd.read_csv(file_path)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found.")
        for value, group in df.groupby(column_name):
            if group.empty:
                continue
            safe_value = str(value).replace("/", "_").replace("\\", "_").replace(":", "_")
            output_file = os.path.join(output_folder, f"{safe_value}.csv")
            group.to_csv(output_file, index=False)
    else:
        raise ValueError("Unsupported file type.")

# ---- Flask Routes ----
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        column_name = request.form.get("column", "").strip()

        if not file or column_name == "":
            return render_template("index.html", message="Please upload a file and enter a column name.")

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        split_folder = os.path.join(OUTPUT_FOLDER, os.path.splitext(filename)[0])
        os.makedirs(split_folder, exist_ok=True)

        try:
            split_file_by_column(file_path, column_name, split_folder)
        except Exception as e:
            return render_template("index.html", message=f"Error: {e}")

        # ✅ Create ZIP file in memory (avoids FileNotFoundError)
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(split_folder):
                for f in files:
                    file_path = os.path.join(root, f)
                    arcname = os.path.relpath(file_path, split_folder)
                    zipf.write(file_path, arcname)
        zip_buffer.seek(0)

        # Optional cleanup of temp files
        for root, _, files in os.walk(split_folder):
            for f in files:
                os.remove(os.path.join(root, f))
        os.rmdir(split_folder)

        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name=f"{os.path.splitext(filename)[0]}_split.zip"
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)