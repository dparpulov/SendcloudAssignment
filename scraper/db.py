def create_all_tables(cursor):
    """
        This function calls all the create table functions at once
        Used to simplify the building of the db
    """
    _create_feed_table(cursor)
    _create_item_table(cursor)
    _create_user_table(cursor)
    _create_follows_table(cursor)
    _create_user_read_item_table(cursor)


def _create_feed_table(cursor):
    """
        This function creates the feed table using the cursor
    """
    cursor.execute(
        """
            CREATE TABLE feed
            (_id integer primary key autoincrement, url text)
        """
    )


def add_feeds(cursor, feeds):
    """
        This function populates the feed table with feeds

        Args:
            feeds (list): A list of feed urls for scraping

        Returns:
            list: The return value is a list of all scraped items
    """
    cursor.executemany("INSERT OR IGNORE INTO feed VALUES(null, ?)",
                       [(f,) for f in feeds])
    return feeds


def _create_item_table(cursor):
    """
        This function creates the item table
    """
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
    """
        This function creates the user table
    """
    cursor.execute(
        """
            CREATE TABLE user
            (_id integer primary key autoincrement)
        """
    )


def add_users(cursor, user_amount):
    """
        This function populates the user table with data

        Args:
            user_amount (int): The number of users to be created
    """
    cursor.executemany(
        "INSERT INTO user VALUES (null)", [() for _ in range(user_amount)]
    )


def _create_follows_table(cursor):
    """
        This function creates the follow table
        It stores which feeds are followed by which user
    """
    cursor.execute(
        """CREATE TABLE follows
            (user_id integer, feed_id integer, 
            primary key (user_id, feed_id), 
            foreign key (user_id) references user(id)
            foreign key (feed_id) references feed(id))
        """
    )


def _create_user_read_item_table(cursor):
    """
        This function creates the user_read_item table
        It stores which items have been read by the users
    """
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


def update_items(cursor, items):
    cursor.executemany(
        """INSERT OR IGNORE INTO item VALUES (null, ?, ?, ?, ?)""", items
    )


def follow_feed(cursor, user_id, feed_id):
    """
        This function checks if the user and feed passed exist
        and adds them to the follows table if they are not there

        Args:
            user_id (int): The id of the user
            feed_id (int): The id of the feed

        Return:
            int: If the ids don't exist or are below 0 the function returns 0
    """
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
    """
        This functions removes a row from the follows table
        if it has the user_id and the feed_id

        Args:
            user_id (int): The id of the user
            feed_id (int): The id of the feed    
    """
    cursor.execute(
        """
        DELETE FROM follows WHERE user_id = ? AND feed_id = ?
        """,
        (user_id, feed_id)
    )


def user_follows(cursor, user_id):
    """
        This functions returns the feed urls that the user follows

        Args:
            user_id (int): The id of the user

        Returns:
            list: returns all the feed urls that the user follows
    """
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
    """
        This function returns all of the items in the item table

        Return:
            list: returns all items from item table
    """
    cursor.execute("SELECT * FROM item")
    items = cursor.fetchall()
    items = [tuple(item) for item in items]

    return items


def get_specific_feed_items(cursor, feed_id):
    """
        This functions return all items that match the feed_id

        Args:
            feed_id (int): The id of the feed

        Returns:
            list: returns all the feed items that match the feed_id
    """
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
    """
        This function checks if the user and item passed exist
        and adds them to the table user_read_item

        Args:
            user_id (int): The id of the user
            item_id (int): The id of the item

        Return:
            int: If the ids don't exist or are below 0 the function returns 0
    """
    cursor.execute("SELECT COUNT(_id) FROM user")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(_id) FROM item")
    total_items = cursor.fetchone()[0]

    if total_users < user_id or total_items < item_id or user_id < 0 or item_id < 0:
        return 0
    else:
        cursor.execute(
            """
                INSERT OR IGNORE INTO user_read_item VALUES (?, ?)
            """,
            (user_id, item_id),
        )


def show_all_read_items(cursor, user_id):
    """
        This function checks if the user has any read items
        and returns them

        Args:
            user_id (int): The id of the user

        Return:
            list: returns all the read items
    """
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
    """
        This function checks if the user has any unread items
        and returns them

        Args:
            user_id (int): The id of the user

        Return:
            list: returns all the unread items
    """
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
    """
        This function checks if the user has any read items
        from a specific feed and returns them

        Args:
            user_id (int): The id of the user
            feed_id (int): The id of the feed

        Return:
            list: returns all the read items from the feed
    """
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
    """
        This function checks if the user has any unread items
        from a specific feed and returns them

        Args:
            user_id (int): The id of the user
            feed_id (int): The id of the feed

        Return:
            list: returns all the unread items from the feed
    """
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
