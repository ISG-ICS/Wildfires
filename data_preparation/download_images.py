from connection import Connection
import os

def get_image_urls(feature=None):  # from database

    return Connection().sql_execute(f"select id, image_url from images")


"""
cnt = 0
while True:
    url = get_image_url(feature)
    cnt +=1
    strcnt = str(cnt)
    os.system(f"curl {url} --output {strcnt}")
"""
if __name__ == '__main__':
    cnt = 0
    for id, image_url in get_image_urls():
        cnt +=1
        strcnt = str(cnt)
        print(strcnt, id, image_url)
        strid = str(id)

        os.system(f"curl {image_url} --output {'../down_image/'+strcnt+'-'+strid+'.jpg'}")
