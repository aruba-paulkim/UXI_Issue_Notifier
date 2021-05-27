#-*-coding:utf-8-*-
#pip install requests Slacker
import requests
import datetime, sys, time, json, urllib3
from slacker import Slacker

urllib3.disable_warnings()

now = datetime.datetime.now()
nowDate = now.strftime('%Y%m%d')

OAuthToken = "SLACK_APP_OAuth_Tokens_start_with_xoxb-..."
APIKEY = "YOUR_UXI_APIKEY"
APPID = "YOUR_UXI_APPID"


def logging(logmsg) :
    f = open("UXI_Issue_Notifier-"+nowDate+".log",'a')
    print(logmsg)
    f.write(logmsg+"\r\n")
    f.close()

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )


def main():

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'X-API-KEY': APIKEY,
        'X-APP-ID': APPID
    }

    url = "https://api.capenetworks.com/v1/nodes"
    response = requests.get(url, headers=headers, verify=False)

    j = response.json()

    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    logging("===== [%s] start =====" % nowDatetime)

    nodes = j['payload']['nodes']
    for node in nodes:
        if node['state'] == "pending" :
            continue

        if node['name'] == "root" :
            continue

        send_msg1 = "%s is %s " % (node['name'], node['state'])
        logging(send_msg1)
        for issue_summary in node['issue_summary']:
            send_msg2 = "- %s device_count is %s " %(issue_summary['code'], issue_summary['device_count'])
            logging(send_msg2)

            # 802.1X authentication failed -> auth error (clearpass)
            if issue_summary['code'] == "WIFI_8021X_AUTHENTICATION_TIMEOUT" and issue_summary['device_count'] > 10 :
                send_msg3 = "- Major Error : %s device_count is %s " %(issue_summary['code'], issue_summary['device_count'])
                post_message(OAuthToken,'#uxi-samsung', send_msg1+"\n"+send_msg3)
                print(send_msg3)

            if issue_summary['code'] == "WIFI_8021X_AUTHENTICATION_TIMEOUT"  and issue_summary['device_count'] > 100 :
                send_msg3 = "- Critical Error : %s device_count is %s " %(issue_summary['code'], issue_summary['device_count'])
                post_message(OAuthToken,'#uxi-samsung', send_msg1+"\n"+send_msg3)
                print(send_msg3)

            # Wi-Fi association failed -> connection error (controller)
            if issue_summary['code'] == "WIFI_ASSOC_TIMEOUT"  and issue_summary['device_count'] > 10:
                send_msg3 = "- Major Error : %s device_count is %s " %(issue_summary['code'], issue_summary['device_count'])
                post_message(OAuthToken,'#uxi-samsung', send_msg1+"\n"+send_msg3)
                print(send_msg3)

            if issue_summary['code'] == "WIFI_ASSOC_TIMEOUT"  and issue_summary['device_count'] > 100:
                send_msg3 = "- Critical Error : %s device_count is %s " %(issue_summary['code'], issue_summary['device_count'])
                post_message(OAuthToken,'#uxi-samsung', send_msg1+"\n"+send_msg3)
                print(send_msg3)

    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    logging("===== [%s] end =====" % nowDatetime)




if __name__ == "__main__":
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()

    print('Duration: {}'.format(end_time - start_time))

