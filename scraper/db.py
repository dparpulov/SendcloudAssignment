from scrape import scrape_feeds


def create_all_tables(cursor):
    _create_feed_table(cursor)
    _create_item_table(cursor)
    _create_user_table(cursor)
    _create_follows_table(cursor)
    _create_user_read_item_table(cursor)


def _create_feed_table(cursor):
    cursor.execute(
        """
            CREATE TABLE feed
            (_id integer primary key autoincrement, url text)
        """
    )


def add_feeds(cursor, feeds):
    cursor.executemany("INSERT OR IGNORE INTO feed VALUES(null, ?)",
                       [(f,) for f in feeds])
    return feeds


def _create_item_table(cursor):
    cursor.execute(
        """
            CREATE TABLE item
            (   
                _id integer primary key autoincrement,
                title text,
                item_url text,
                published datetime,
                feed_url text,
                UNIQUE(title)
            )
        """
    )


def _create_user_table(cursor):
    cursor.execute(
        """
            CREATE TABLE user
            (_id integer primary key autoincrement)
        """
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


def get_feeds(cursor):
    return [row[0] for row in cursor.execute("SELECT url FROM feed")]


def update_items(cursor):
    items = scrape_feeds(get_feeds(cursor))
    items = [tuple(item.values()) for item in items]
    cursor.executemany(
        """INSERT OR IGNORE INTO item VALUES (null, ?, ?, ?, ?)""", items
    )


def follow_feed(cursor, user_id, feed_id):
    cursor.execute("SELECT COUNT(_id) FROM user")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(_id) FROM feed")
    total_feeds = cursor.fetchone()[0]

    if total_users < user_id or total_feeds < feed_id or user_id < 0 or feed_id < 0:
        return 0
    else:
        cursor.execute(
            """
                INSERT OR IGNORE INTO follows VALUES (?, ?)
            """, (user_id, feed_id))


def unfollow_feed(cursor, user_id, feed_id):
    cursor.execute(
        """
        DELETE FROM follows WHERE user_id = ? AND feed_id = ?
        """,
        (user_id, feed_id)
    )


def user_follows(cursor, user_id):
    cursor.execute(
        """
            SELECT url
            FROM feed
            JOIN follows ON feed_id = feed._id
            WHERE user_id = ?
        """,
        (user_id,),
    )
    return [row[0] for row in cursor.fetchall()]


def get_all_items(cursor):
    cursor.execute("SELECT * FROM item")
    items = cursor.fetchall()
    items = [tuple(item) for item in items]

    return items


def get_specific_feed_items(cursor, feed_id):
    cursor.execute(
        """
            SELECT *
            FROM item
            WHERE feed_url = (SELECT url
                              FROM feed
                              WHERE _id = ?)
        """,
        (feed_id,)
    )
    items = [item for item in cursor.fetchall()]
    return items


def add_read_item(cursor, user_id, item_id):
    cursor.execute("SELECT COUNT(_id) FROM user")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(_id) FROM item")
    total_items = cursor.fetchone()[0]

    if total_users < user_id or total_items < item_id or user_id < 0 or item_id < 0:
        return 0
    else:
        cursor.execute(
            """
                INSERT INTO user_read_item VALUES (?, ?)
            """,
            (user_id, item_id),
        )


def show_all_read_items(cursor, user_id):
    cursor.execute(
        """
            SELECT *
            FROM item
            WHERE _id IN (SELECT item_id
                        FROM user_read_item
                        WHERE user_id = ?)
            ORDER BY published DESC
        """,
        (user_id,),
    )
    items = [tuple(item) for item in cursor.fetchall()]
    return items


def show_all_unread_items(cursor, user_id):
    cursor.execute(
        """
            SELECT *
            FROM item
            WHERE _id NOT IN (SELECT item_id
                            FROM user_read_item
                            WHERE user_id = ?)
            ORDER BY published DESC
        """,
        (user_id,),
    )
    items = [tuple(item) for item in cursor.fetchall()]
    return items


def show_read_items_feed(cursor, user_id, feed_id):
    cursor.execute(
        """
            SELECT *
            FROM item
            WHERE _id IN (
                        SELECT item_id
                        FROM user_read_item
                        WHERE user_id = ? )
            AND feed_url IN (
                        SELECT url
                        FROM feed
                        WHERE _id = ?)
            ORDER BY published DESC            
        """,
        (user_id, feed_id),
    )
    items = [tuple(item) for item in cursor.fetchall()]
    return items


def show_unread_items_feed(cursor, user_id, feed_id):
    cursor.execute(
        """
            SELECT *
            FROM item
            WHERE _id NOT IN (SELECT item_id
                        FROM user_read_item
                        WHERE user_id = ? )
            AND feed_url IN (
                        SELECT url
                        FROM feed
                        WHERE _id = ?)
            ORDER BY published DESC            
        """,
        (user_id, feed_id),
    )
    items = [tuple(item) for item in cursor.fetchall()]
    return items
