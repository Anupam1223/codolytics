# import lzma
import pandas as pd
from ariadne import QueryType
from graphql import GraphQLResolveInfo

from app.services.metrics import Metrics

metrics_type = QueryType()

# summary of active developers, Inactive developers, Code commits, PR activity
# Developer status - developer, total LOC, total commits, total PR activity
# Work log - Authors with number of commit per year along with the size of each commit


@metrics_type.field("projectSummary")
async def resolve_project_summary(_, info: GraphQLResolveInfo, after=None, before=None):
    df = pd.read_pickle("app/logs/react-logs.xz")
    metrics = Metrics(df)
    project_summary = await metrics.project_summary(after, before)
    return {
        "totalDevelopers": project_summary["total_developers"],
        "activeDevelopers": project_summary["active_developers"],
        "inactiveDevelopers": project_summary["inactive_developers"],
        "totalCommits": project_summary["total_commits"],
    }


@metrics_type.field("developerStatus")
async def resolve_summary_of_each_author(
    _, info: GraphQLResolveInfo, after=None, before=None
):
    df = pd.read_pickle("app/logs/react-logs.xz")
    metrics = Metrics(df)
    developer_status = await metrics.summary_of_each_author(after, before)
    return developer_status


@metrics_type.field("commitActivities")
async def resolve_commit_activities(
    _, info: GraphQLResolveInfo, after=None, before=None
):
    df = pd.read_pickle("app/logs/react-logs.xz")
    metrics = Metrics(df)
    commit_activities = await metrics.commit_activities(after, before)
    return [commit_activities]


@metrics_type.field("workLogs")
async def resolve_work_logs(_, info: GraphQLResolveInfo, after, before):
    df = pd.read_pickle("app/logs/react-logs.xz")
    metrics = Metrics(df)
    work_logs = await metrics.work_logs(after, before)
    return work_logs
