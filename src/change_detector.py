"""
Change Detector Module
Detects and tracks changes in competitor content over time
"""

import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json
import difflib


class ChangeDetector:
    """Detects and stores changes in competitor content"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table for storing page snapshots
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS page_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competitor TEXT NOT NULL,
                page_type TEXT NOT NULL,
                url TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                title TEXT,
                meta_description TEXT,
                main_content TEXT,
                markdown TEXT,
                priority TEXT,
                fetched_at TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Table for detected changes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detected_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competitor TEXT NOT NULL,
                page_type TEXT NOT NULL,
                url TEXT NOT NULL,
                change_type TEXT NOT NULL,
                change_summary TEXT,
                old_snapshot_id INTEGER,
                new_snapshot_id INTEGER,
                detected_at TEXT DEFAULT CURRENT_TIMESTAMP,
                priority TEXT,
                analyzed BOOLEAN DEFAULT 0,
                FOREIGN KEY (old_snapshot_id) REFERENCES page_snapshots(id),
                FOREIGN KEY (new_snapshot_id) REFERENCES page_snapshots(id)
            )
        ''')

        # Index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_competitor_page
            ON page_snapshots(competitor, page_type, url)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_changes_analyzed
            ON detected_changes(analyzed, detected_at)
        ''')

        conn.commit()
        conn.close()

    def store_snapshot(self, page_data: Dict) -> int:
        """
        Store a page snapshot in the database

        Returns:
            Snapshot ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO page_snapshots
            (competitor, page_type, url, content_hash, title, meta_description,
             main_content, markdown, priority, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            page_data['competitor'],
            page_data['page_type'],
            page_data['url'],
            page_data['content_hash'],
            page_data.get('title', ''),
            page_data.get('meta_description', ''),
            page_data.get('main_content', ''),
            page_data.get('markdown', ''),
            page_data.get('priority', 'medium'),
            page_data['fetched_at']
        ))

        snapshot_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return snapshot_id

    def get_latest_snapshot(self, competitor: str, page_type: str, url: str) -> Optional[Dict]:
        """Get the most recent snapshot for a specific page"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM page_snapshots
            WHERE competitor = ? AND page_type = ? AND url = ?
            ORDER BY fetched_at DESC
            LIMIT 1
        ''', (competitor, page_type, url))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def detect_change(self, new_data: Dict) -> Optional[Dict]:
        """
        Detect if content has changed compared to the last snapshot

        Returns:
            Change dictionary if change detected, None otherwise
        """
        # Get the latest snapshot for this page
        latest = self.get_latest_snapshot(
            new_data['competitor'],
            new_data['page_type'],
            new_data['url']
        )

        # If no previous snapshot, this is the first scan
        if not latest:
            return None

        # Check if content hash changed
        if latest['content_hash'] == new_data['content_hash']:
            return None  # No change

        # Content changed - analyze what changed
        change_summary = self._analyze_change(
            latest['main_content'],
            new_data['main_content'],
            latest['title'],
            new_data.get('title', '')
        )

        change = {
            'competitor': new_data['competitor'],
            'page_type': new_data['page_type'],
            'url': new_data['url'],
            'change_type': self._categorize_change(change_summary),
            'change_summary': json.dumps(change_summary),
            'old_snapshot_id': latest['id'],
            'priority': new_data.get('priority', 'medium')
        }

        return change

    def _analyze_change(self, old_content: str, new_content: str,
                       old_title: str, new_title: str) -> Dict:
        """Analyze what changed between two versions"""
        changes = {
            'title_changed': old_title != new_title,
            'content_length_diff': len(new_content) - len(old_content),
            'substantial_change': False,
            'added_keywords': [],
            'removed_keywords': []
        }

        # Title change
        if changes['title_changed']:
            changes['old_title'] = old_title
            changes['new_title'] = new_title

        # Substantial content change (more than 10% difference)
        if old_content and new_content:
            ratio = difflib.SequenceMatcher(None, old_content, new_content).ratio()
            changes['similarity_ratio'] = round(ratio, 3)
            changes['substantial_change'] = ratio < 0.9

            # Extract some context about what changed
            if changes['substantial_change']:
                differ = difflib.Differ()
                diff = list(differ.compare(old_content.split(), new_content.split()))

                # Find added and removed words
                added = [word[2:] for word in diff if word.startswith('+ ')][:10]
                removed = [word[2:] for word in diff if word.startswith('- ')][:10]

                changes['added_keywords'] = added
                changes['removed_keywords'] = removed

        return changes

    def _categorize_change(self, change_summary: Dict) -> str:
        """Categorize the type of change"""
        if change_summary.get('title_changed'):
            return 'title_change'
        elif change_summary.get('substantial_change'):
            return 'major_content_change'
        elif abs(change_summary.get('content_length_diff', 0)) > 500:
            return 'content_update'
        else:
            return 'minor_change'

    def record_change(self, change: Dict, new_snapshot_id: int):
        """Record a detected change in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO detected_changes
            (competitor, page_type, url, change_type, change_summary,
             old_snapshot_id, new_snapshot_id, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            change['competitor'],
            change['page_type'],
            change['url'],
            change['change_type'],
            change['change_summary'],
            change['old_snapshot_id'],
            new_snapshot_id,
            change['priority']
        ))

        conn.commit()
        conn.close()

    def get_unanalyzed_changes(self) -> List[Dict]:
        """Get all changes that haven't been analyzed by AI yet"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.*,
                   old.main_content as old_content,
                   new.main_content as new_content,
                   old.title as old_title,
                   new.title as new_title
            FROM detected_changes c
            LEFT JOIN page_snapshots old ON c.old_snapshot_id = old.id
            LEFT JOIN page_snapshots new ON c.new_snapshot_id = new.id
            WHERE c.analyzed = 0
            ORDER BY c.detected_at DESC
        ''')

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def mark_change_analyzed(self, change_id: int):
        """Mark a change as analyzed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE detected_changes
            SET analyzed = 1
            WHERE id = ?
        ''', (change_id,))

        conn.commit()
        conn.close()

    def get_recent_changes(self, days: int = 7) -> List[Dict]:
        """Get all changes from the last N days"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM detected_changes
            WHERE detected_at >= datetime('now', '-' || ? || ' days')
            ORDER BY detected_at DESC
        ''', (days,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_competitor_history(self, competitor: str, page_type: str = None) -> List[Dict]:
        """Get change history for a specific competitor"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if page_type:
            cursor.execute('''
                SELECT * FROM detected_changes
                WHERE competitor = ? AND page_type = ?
                ORDER BY detected_at DESC
            ''', (competitor, page_type))
        else:
            cursor.execute('''
                SELECT * FROM detected_changes
                WHERE competitor = ?
                ORDER BY detected_at DESC
            ''', (competitor,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
