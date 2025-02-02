import pandas as pd

# import ast
from models import db, Game


def csv2db():
    media_df = pd.read_csv("ja_media.csv", index_col=0)
    # videos_list = ast.literal_eval(media_df.at[1245620, "videos"])
    # データベースに保存
    for index, row in media_df.iterrows():
        game = Game(
            appid=index,
            name=row["name"],
            publisher=row["publisher"],
            short_description=row["short_description"],
            videos=row["videos"],
            thumbnails=row["thumbnails"],
        )
        db.session.add(game)
        db.session.commit()


if __name__ == "__main__":
    csv2db()
