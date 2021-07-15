from ariadne import QueryType
from graphql import GraphQLResolveInfo

from app.gitdataminer.src.gitdataminer import gitlogs

metrics_type = QueryType()

# summary of active developers, Inactive developers, Code commits, PR activity
# Developer status - developer, total LOC, total commits, total PR activity
# Work log - Authors with number of commit per year along with the size of each commit


@metrics_type.field("projectSummary")
async def resolve_project_summary(_, info: GraphQLResolveInfo, after=None, before=None):
    log_metrics = gitlogs.CommitAnalyzer("app/logs/react-git.log")
    project_summary = await log_metrics.project_summary(after, before)
    return {
        "totalDevelopers": project_summary["total_developers"],
        "activeDevelopers": project_summary["active_developers"],
        "inactiveDevelopers": project_summary["inactive_developers"],
        "totalCommits": project_summary["total_commits"],
    }


@metrics_type.field("developerStatus")
async def resolve_developer_status(
    _, info: GraphQLResolveInfo, after=None, before=None
):
    log_metrics = gitlogs.CommitAnalyzer("app/logs/react-git.log")
    author_summary = await log_metrics.summary_of_each_author(after, before)
    author_summary_json = author_summary.to_dict("records")
    return author_summary_json


@metrics_type.field("commitActivities")
async def resolve_commit_activities(
    _, info: GraphQLResolveInfo, after=None, before=None
):
    log_metrics = gitlogs.CommitAnalyzer("app/logs/react-git.log")
    commit_activities = await log_metrics.commit_activity(after, before)
    response = [
        {
            "totalCodingHours": commit_activities["total_coding_hours"],
            "averageCodingHours": commit_activities["average_coding_hours"],
            "totalAuthors": commit_activities["total_authors"],
            "filesChanged": commit_activities["files_changed"],
            "insertionCount": commit_activities[
                "insertion_count"
            ],  # treated as productive for now
            "deletionCount": commit_activities[
                "deletion_count"
            ],  # treated as unproductive for now
            "totalLines": commit_activities["total_lines"],
            "addDelRatio": commit_activities["add_del_ratio"],
        }
    ]
    return response


@metrics_type.field("workLogs")
async def resolve_work_logs(_, info: GraphQLResolveInfo, after, before):
    log_metrics = gitlogs.CommitAnalyzer("app/logs/react-git.log")
    work_logs = await log_metrics.commit_logs_per_day(after, before)
    if len(work_logs):
        result = [
            #     key: group.reset_index(level=0, drop=True).to_dict(orient='index')
            {
                "author": key,
                "commitInfo": group.to_dict(orient="records"),
                "timestamp": [index[1] for index in list(group.index)],
            }
            for key, group in work_logs.groupby("author")
        ]
        print("result", result)
        return result
    return []
