## email part
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


def set_up_email(host_server,sender_qq,pwd):
    smtp = SMTP_SSL(host_server)
    print(smtp)
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(sender_qq,pwd)
    return smtp
def send_email(smtp,mail_title,mail_content,sender_qq_mail,receiver):
    msg = MIMEText(mail_content, "html", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()

def get_html_msg(df):
    """
    1. 构造html信息
    """
    df_html = df.to_html(escape=False)
    head = \
        """
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>

                table.dataframe {
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                    /*居中显示整个表格*/
                    margin: auto;
                }

                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }

                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }

                table.dataframe tr {

                }

                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }

                table.dataframe td {
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                }

                body {
                    font-family: 宋体;
                }

                h1 {
                    color: #5db446
                }

                div.header h2 {
                    color: #0002e3;
                    font-family: 黑体;
                }

                div.content h2 {
                    text-align: center;
                    font-size: 28px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5px #888888;
                    border-radius: 5px;
                }

                h3 {
                    font-size: 22px;
                    background-color: rgba(0, 2, 227, 0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239, 241, 234, 0.99);
                    line-height: 1.5;
                }

                h4 {
                    color: #e10092;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }

                td img {
                    /*width: 60px;*/
                    max-width: 300px;
                    max-height: 300px;
                }

            </STYLE>
        </head>
        """
    body = \
        """
        <body>

        <div align="center" class="header">
            <h1 align="center">调剂反馈</h1>
        </div>

        <hr>

        <div class="content">
            <!--正文内容-->
            <h2>您当前的可调剂信息</h2>

            <div>
                <h4></h4>
                {df_html}

            </div>
            <hr>

            <p style="text-align: center">
                —— 您已经到底底部 ——
            </p>
        </div>
        </body>
        """.format(df_html=df_html)
    html_msg= "<html>" + head + body + "</html>"
    # 这里是将HTML文件输出，作为测试的时候，查看格式用的，正式脚本中可以注释掉
    #fout = open('t4.html', 'w', encoding='UTF-8', newline='')
    #fout.write(html_msg)
    return html_msg
