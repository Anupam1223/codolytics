from datetime import timedelta

import pandas as pd

from .utils import lines_of_code_changes_per_project, total_coding_hours_of_all_author


class Metrics:
    def __init__(self, df):
        self.df = df

    async def list_of_developers(self):
        return pd.unique(self.df["author"])

    async def total_developers(self):
        return len(pd.unique(self.df["author"]))

    async def total_coding_hours_of_all_author(self):
        return await total_coding_hours_of_all_author(self.df)

    async def project_summary(self, after=None, before=None):
        if after is None or before is None:
            today = pd.to_datetime("today", utc=True)
            after = pd.to_datetime(today - timedelta(days=today.weekday()), utc=True)
            before = pd.to_datetime(after + timedelta(days=6), utc=True)
        filter_df = self.df[(self.df["date"] > after) & (self.df["date"] < before)]
        total_developers = await self.total_developers()
        active_developers = len(pd.unique(filter_df["author"]))
        inactive_developers = total_developers - active_developers
        total_commits = self.df["sha"].nunique()
        return {
            "filter_df": filter_df,
            "total_developers": total_developers,
            "active_developers": active_developers,
            "inactive_developers": inactive_developers,
            "total_commits": total_commits,
        }

    async def summary_of_each_author(self, after=None, before=None):
        if after is None or before is None:
            today = pd.to_datetime("today", utc=True)
            after = pd.to_datetime(today - timedelta(days=today.weekday()), utc=True)
            before = pd.to_datetime(after + timedelta(days=6), utc=True)
        filter_df = self.df[(self.df["date"] > after) & (self.df["date"] < before)]
        author_with_commit_df = (
            filter_df.groupby("author")["sha"].nunique().sort_values(ascending=False)
        )
        author_with_insertion_deletion = filter_df.groupby("author").sum()[
            ["insertion", "deletion"]
        ]
        author_summary_df = pd.merge(
            author_with_commit_df, author_with_insertion_deletion, on=["author"]
        )
        author_summary_df["totalLOC"] = (
            author_summary_df["insertion"] - author_summary_df["deletion"]
        )
        author_summary_df["author"] = author_summary_df.index
        author_summary_json = author_summary_df.head(5).to_dict("records")
        return author_summary_json

    async def commit_activities(self, after=None, before=None):
        total_coding_hours_df = await self.total_coding_hours_of_all_author()
        (
            files_changed,
            insertion_count,
            deletion_count,
            total_lines,
            add_del_ratio,
        ) = await self.lines_of_code_changes_per_project()
        total_coding_hours = total_coding_hours_df["hours"].sum()
        average_coding_hours = total_coding_hours_df["hours"].mean()
        # total_authors
        total_authors = await self.total_developers()
        # lines_of_code_changes_per_project
        return {
            "totalCodingHours": total_coding_hours,
            "averageCodingHours": average_coding_hours,
            "totalAuthors": total_authors,
            "filesChanged": files_changed,
            "insertionCount": insertion_count,
            "deletionCount": deletion_count,
            "totalLines": total_lines,
            "addDelRatio": add_del_ratio,
        }

    async def work_logs(self, after=None, before=None):
        if after is None or before is None:
            today = pd.to_datetime("today", utc=True)
            after = pd.to_datetime(today - timedelta(days=today.weekday()), utc=True)
            before = pd.to_datetime(after + timedelta(days=6), utc=True)
        filter_df = self.df[(self.df["date"] > after) & (self.df["date"] < before)]
        print("filter_df.size", filter_df.size)
        if filter_df.size:
            timed_commits = filter_df.set_index("date")
            grouped = timed_commits.groupby(by=["author"])
            resampled = grouped.resample("D").agg(
                {
                    "sha": "size",
                    "insertion": "sum",
                    "deletion": "sum",
                    "filepath": "size",
                }
            )
            print("resampled", resampled.size)
            # need to convert it to dict
            if resampled.size:
                result = [
                    #     key: group.reset_index(level=0, drop=True).to_dict(orient='index')
                    {
                        "author": key,
                        "commitInfo": group.to_dict(orient="records"),
                        "timestamp": [index[1] for index in list(group.index)],
                    }
                    for key, group in resampled.groupby("author")
                ]
                return result
            else:
                return []
        else:
            return []

    async def lines_of_code_changes_per_project(self):
        return await lines_of_code_changes_per_project(self.df)
