#!/usr/bin/env python3
"""
Migration script to add created_at and updated_at columns to existing posts.

This script:
1. Adds created_at and updated_at columns to the posts table
2. Populates them with values based on the existing date field
3. For posts with the same date, uses ID to determine order (lower ID = earlier time)
"""

import sqlite3
from datetime import datetime, timedelta

DATABASE = 'blog.db'

def migrate():
    """Add timestamp columns and populate with data"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("Starting migration...")

    # Check if columns already exist
    cursor.execute("PRAGMA table_info(posts)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'created_at' in columns and 'updated_at' in columns:
        print("✓ Columns already exist. Checking if they need to be populated...")

        # Check if any posts have NULL timestamps
        cursor.execute("SELECT COUNT(*) FROM posts WHERE created_at IS NULL OR updated_at IS NULL")
        null_count = cursor.fetchone()[0]

        if null_count == 0:
            print("✓ All posts already have timestamps. Migration complete!")
            conn.close()
            return
        else:
            print(f"  Found {null_count} posts with NULL timestamps. Populating...")
    else:
        # Add the columns
        print("Adding created_at and updated_at columns...")
        try:
            cursor.execute("ALTER TABLE posts ADD COLUMN created_at DATETIME")
            cursor.execute("ALTER TABLE posts ADD COLUMN updated_at DATETIME")
            print("✓ Columns added successfully")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print("✓ Columns already exist")
            else:
                raise

    # Get all posts ordered by date and ID
    cursor.execute("SELECT id, date FROM posts ORDER BY date ASC, id ASC")
    posts = cursor.fetchall()

    print(f"\nPopulating timestamps for {len(posts)} posts...")

    # Group posts by date
    posts_by_date = {}
    for post in posts:
        date = post['date']
        if date not in posts_by_date:
            posts_by_date[date] = []
        posts_by_date[date].append(post['id'])

    # Update each post with a timestamp
    update_count = 0
    for date_str, post_ids in posts_by_date.items():
        # Parse the date (YYYY-MM-DD format)
        try:
            base_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print(f"  Warning: Invalid date format '{date_str}', using current date")
            base_date = datetime.now()

        # For posts on the same date, assign times throughout the day
        # This preserves the ID-based ordering
        for i, post_id in enumerate(post_ids):
            # Spread posts across the day based on their position
            # First post at 09:00, spread subsequent posts evenly
            if len(post_ids) == 1:
                hours_offset = 12  # Noon
                minutes_offset = 0
            else:
                # Spread from 09:00 to 20:00 (11 hours = 660 minutes)
                time_range = 660
                time_increment = time_range / len(post_ids)
                total_minutes = int(540 + (i * time_increment))  # 540 = 9 AM
                hours_offset = total_minutes // 60
                minutes_offset = total_minutes % 60

            timestamp = base_date.replace(hour=hours_offset, minute=minutes_offset, second=0)
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

            # Update the post
            cursor.execute("""
                UPDATE posts
                SET created_at = ?, updated_at = ?
                WHERE id = ?
            """, (timestamp_str, timestamp_str, post_id))
            update_count += 1

    conn.commit()
    print(f"✓ Updated {update_count} posts with timestamps")

    # Verify the migration
    cursor.execute("SELECT COUNT(*) FROM posts WHERE created_at IS NULL OR updated_at IS NULL")
    null_count = cursor.fetchone()[0]

    if null_count == 0:
        print("\n✓ Migration completed successfully!")
        print("\nSample of migrated data:")
        cursor.execute("""
            SELECT id, title, date, created_at, updated_at
            FROM posts
            ORDER BY created_at DESC
            LIMIT 5
        """)
        for post in cursor.fetchall():
            print(f"  ID {post[0]}: {post[1][:50]}")
            print(f"    Date: {post[2]}, Created: {post[3]}")
    else:
        print(f"\n⚠ Warning: {null_count} posts still have NULL timestamps")

    conn.close()

if __name__ == '__main__':
    try:
        migrate()
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
