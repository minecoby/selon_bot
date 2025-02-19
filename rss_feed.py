import discord
import feedparser
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from model import Notice
from variable import *
from database import *

async def check_rss_feed(bot):
    """ 주기적으로 RSS를 확인하고 새로운 게시글이 있으면 디스코드 전송 """
    await bot.wait_until_ready()
    channel = bot.get_channel(int(CHANNEL_ID))

    while not bot.is_closed():
        session = notice_SessionLocal()
        feed = feedparser.parse(RSS_FEED_URL)
        existing_links = {row[0] for row in session.query(Notice.link).all()}
        new_entries = []

        for entry in feed.entries:
            post_id = entry.link 
            pub_date = datetime(*entry.published_parsed[:6]) if hasattr(entry, "published_parsed") else datetime.utcnow()
            author = entry.author if hasattr(entry, "author") else "Unknown"
            
            if post_id not in existing_links:
                new_entries.append({
                    "id": post_id,
                    "title": entry.title,
                    "link": entry.link,
                    "pubDate": pub_date,
                    "author": author,
                })

        # 새로운 게시글이 있을때 전송하기
        if new_entries:
            for post in new_entries:
                embed = discord.Embed(title=post["title"], url=post["link"], color=discord.Color.blue())
                embed.add_field(name="작성자", value=post["author"], inline=True)
                embed.add_field(name="게시일", value=post["pubDate"].strftime("%Y-%m-%d %H:%M"), inline=True)
                await channel.send(embed=embed)

                new_notice = Notice(
                    title=post["title"],
                    link=post["link"],
                    pubDate=post["pubDate"],
                    author=post["author"],
                )
                session.add(new_notice)
            print(datetime.now().strftime("%Y-%m-%d %H:%M") + " 게시글이 업데이트 되었습니다.")
            session.commit()
            cleanup_database(session)  

        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M") + " 새로운 게시글이 없습니다.")

        session.close()
        await asyncio.sleep(600)  

def cleanup_database(session: Session):
    """ DB 크기 제한을 초과하면 오래된 게시글 삭제 """
    total_entries = session.query(Notice).count()
    if total_entries > int(MAX_DB_SIZE):
        oldest_entries = session.query(Notice).order_by(Notice.pubDate.asc()).limit(total_entries - int(MAX_DB_SIZE))
        for entry in oldest_entries:
            session.delete(entry)
        session.commit()