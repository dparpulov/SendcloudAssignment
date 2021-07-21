
def create_all_tables(cursor):
    _create_feed_table(cursor)
    _create_item_table(cursor)
    _create_user_table(cursor)
    _create_follows_table(cursor)
    _create_user_read_item_table(cursor)


def _create_feed_table(cursor):
    cursor.execute(
        """CREATE TABLE feed
                (_id integer primary key autoincrement, url text)"""
    )


def add_feeds(cursor, feeds):
    cursor.executemany("INSERT INTO feed VALUES(null, ?)",
                       [(f,) for f in feeds])
    return feeds


def _create_item_table(cursor):
    cursor.execute(
        """CREATE TABLE item
            (       _id integer primary key autoincrement,
                    title text,
                    item_url text,
                    published datetime,
                    feed_url text,
                    UNIQUE(title))"""
    )


def _create_user_table(cursor):
    cursor.execute(
        """CREATE TABLE user
                (_id integer primary key autoincrement)"""
    )


def add_users(cursor, user_amount):
    cursor.executemany(
        "INSERT INTO user VALUES (null)", [() for _ in range(user_amount)]
    )


def _create_follows_table(cursor):
    cursor.execute(
        """CREATE TABLE follows
                (user_id integer, feed_id integer, 
                primary key (user_id, feed_id), 
                foreign key (user_id) references user(id)
                foreign key (feed_id) references feed(id))
                """
    )


def _create_user_read_item_table(cursor):
    cursor.execute(
        """CREATE TABLE user_read_item
                (user_id integer, item_id integer, 
                primary key (user_id, item_id), 
                foreign key (user_id) references user(id)
                foreign key (item_id) references item(id))
                """
    )
