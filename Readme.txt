Ultimate_crawl_artistname:
這隻先從Ultimate Guitar Tab網站上爬Pop music的歌手名字與每個歌手的URL下來
之後就可以針對每個歌手的URL把歌手的所有譜抓下來

Ultimate_craw:

先從Mongo,Ultimate_Guitar_Artist資料表把流行樂歌手的url撈出來
例如:想抓beatles的吉他譜，先拿到URL:https://www.ultimate-guitar.com/artist/the_beatles_1916
然後就會看到beatles所有的歌
選擇type=chord的吉他譜

然後就可以用Ultimate_craw透過歌手URL把每個歌手的所有吉他譜抓下來，存在Mongo DB(先抓HTML存Mongo，再撈出來解析，以免資料不見又要重爬)

Ultimate_craw_TabHtmlParse:
這支把爬下來的HTML從MongoDB撈出來並解析HTML以取得資訊(歌手、歌名、歌曲和弦、曲譜Rating等等)並存回MongoDB

~~~~~~以上是爬蟲的部分


GuitarChordPreprocessing:
這支把吉他譜資訊從MongdDB撈出來做資料前處理，
做的事情包刮:所有歌曲轉成C調和弦、將歌曲的和弦做成Hot encoding矩陣


pyace:
和弦辨識套件模組，內含pretrained Rnn Model


DataMerge:
這隻把每首歌曲和弦與吉他譜和弦merge在一起，並且把每張吉他譜的和弦轉為與期對應的歌曲同一個調
做的事情包括:和弦的label_reduce(cleaning)、和弦轉調