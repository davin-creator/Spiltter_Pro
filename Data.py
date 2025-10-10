import requests
import time

api = "eyJhbGciOiJBMjU2S1ciLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiSldUIiwiemlwIjoiREVGIn0.tRoDMOFNalwGXpxnmOGKXm0soao7TvY9-wihT8SIUKt9-K3lb3j53Q.4OBYp5m6CqYX36dd.5gw2VHvZ7Y5w3jlhFGKVOCXFqXC4BnOgXkqq1l_WxKwnipJcaB_s4-w19nx29qF5rl1gDhgWEopGEiasmJYrJgPZrwTyhRfTfeH5YBbDSZdk-BYb2KiSiAMcy3UJcOUVnq-ExbfsA1Yx3M4ZcHQ7xMhKfoXnyuTnOmEsPQtMPk2tbjt2vrDFyPXYbEm2wTkCUC9RCYSiCq_FYODmPM0HSfV0DkfSZQ3gjfJikMHtiENO8AO0E4AkjRdIZoR65eADAyC7SC0SPg4zg24AZFAFobdNXeWevvQicGBq3n1NbrlRGQl0uRsVcWJhSclSLHK9caGDfG0cQd168l1VAKgMoZ6P.tXRDVOty7sjC7auEZAHN4Q"

app_id = "com.bancomer.mbanking"
url = f"https://hq1.appsflyer.com/{api}/raw-data/export/app/{app_id}/installs_report/v5?additional_fields=store_reinstall,impressions,contributor3_match_type,custom_dimension,conversion_type,gp_click_time,match_type,mediation_network,oaid,deeplink_url,blocked_reason,blocked_sub_reason,gp_broadcast_referrer,gp_install_begin,campaign_type,custom_data,rejected_reason,device_download_time,keyword_match_type,contributor1_match_type,contributor2_match_type,device_model,monetization_network,segment,is_lat,gp_referrer,blocked_reason_value,store_product_page,device_category,app_type,rejected_reason_value,ad_unit,keyword_id,placement,network_account_id,install_app_store,amazon_aid,att,engagement_type,contributor1_engagement_type,contributor2_engagement_type,contributor3_engagement_type,gdpr_applies,ad_user_data_enabled,ad_personalization_enabled,total_candidates"

headers_pro = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0 Safari/537.36"}

# Initial POST request to start the process
initial_response = requests.get(f"https://hq1.appsflyer.com/eyJhbGciOiJBMjU2S1ciLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiSldUIiwiemlwIjoiREVGIn0.tRoDMOFNalwGXpxnmOGKXm0soao7TvY9-wihT8SIUKt9-K3lb3j53Q.4OBYp5m6CqYX36dd.5gw2VHvZ7Y5w3jlhFGKVOCXFqXC4BnOgXkqq1l_WxKwnipJcaB_s4-w19nx29qF5rl1gDhgWEopGEiasmJYrJgPZrwTyhRfTfeH5YBbDSZdk-BYb2KiSiAMcy3UJcOUVnq-ExbfsA1Yx3M4ZcHQ7xMhKfoXnyuTnOmEsPQtMPk2tbjt2vrDFyPXYbEm2wTkCUC9RCYSiCq_FYODmPM0HSfV0DkfSZQ3gjfJikMHtiENO8AO0E4AkjRdIZoR65eADAyC7SC0SPg4zg24AZFAFobdNXeWevvQicGBq3n1NbrlRGQl0uRsVcWJhSclSLHK9caGDfG0cQd168l1VAKgMoZ6P.tXRDVOty7sjC7auEZAHN4Q/raw-data/export/app/com.bancomer.mbanking/installs_report/v5?additional_fields=store_reinstall,impressions,contributor3_match_type,custom_dimension,conversion_type,gp_click_time,match_type,mediation_network,oaid,deeplink_url,blocked_reason,blocked_sub_reason,gp_broadcast_referrer,gp_install_begin,campaign_type,custom_data,rejected_reason,device_download_time,keyword_match_type,contributor1_match_type,contributor2_match_type,device_model,monetization_network,segment,is_lat,gp_referrer,blocked_reason_value,store_product_page,device_category,app_type,rejected_reason_value,ad_unit,keyword_id,placement,network_account_id,install_app_store,amazon_aid,att,engagement_type,contributor1_engagement_type,contributor2_engagement_type,contributor3_engagement_type,gdpr_applies,ad_user_data_enabled,ad_personalization_enabled,total_candidates"
, headers=headers_pro)

if initial_response.status_code == 202:
    print("Request accepted for processing.")
    # Extract the URL for checking status/results (e.g., from 'Location' header)
    status_url = initial_response.headers.get("Location") or initial_response.headers.get("status_url")

    if status_url:
        # Poll the status URL until the task is complete
        while True:
            status_response = requests.get(status_url)
            if status_response.status_code == 200:
                print("Task completed. Data retrieved:")
                print(status_response.json())
                break
            elif status_response.status_code == 202:
                print("Task still in progress. Waiting...")
                time.sleep(5)  # Wait for 5 seconds before polling again
            else:
                print(f"Error checking status: {status_response.status_code}")
                break
    else:
        print("No status URL provided in the 202 response.")
else:
    print(f"Unexpected initial response status: {initial_response.status_code}")