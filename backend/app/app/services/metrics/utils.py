import pandas as pd


async def total_coding_hours_of_all_author(df):
    """
    get the hours estimate for this repository (using 30 mins per commit)
    of time indicated by limit/extensions/days/etc.
    For each author in the commit history, do the following:
        1. Go through all commits and compare the difference between them in time.
        2. If the difference is smaller or equal then a given threshold, group the
        commits to a same coding session.(Time between commits < 1h yes then group
        those commits as same coding session)
        3. If the difference is bigger than a given threshold, the coding session
        is finished.
        4. To compensate the first commit whose work is unknown, we add extra hours
        to the coding session.
        5. Continue until we have determined all coding sessions and sum the hours
        made by individual authors

    """
    # the threhold for how close two commits need to be to consider them
    # part of one coding session
    grouping_window = 0.5
    single_commit_hours = 0.5  # the time range to associate with one single commit
    # Maximum time diff between 2 subsequent commits in minutes which are
    # counted to be in the same coding "session"
    max_commit_diff_in_minutes = grouping_window * 60.0
    first_commit_addition_in_minutes = single_commit_hours * 60.0
    people = set(df["author"].values)
    ds = []
    commit_df_copy = df.loc[:]
    commit_df_copy.set_index(keys=["date"], drop=True, inplace=True)
    for person in people:
        commits = commit_df_copy[commit_df_copy["author"] == person]
        commits_ts = [x * 10e-10 for x in sorted(commits.index.values.tolist())]
        if len(commits_ts) < 2:
            ds.append([person, 0])
            continue

        async def estimate(index, date):
            next_ts = commits_ts[index + 1]
            diff_in_minutes = next_ts - date
            diff_in_minutes /= 60.0
            # steps 2 - Check if commits are counted to be in same coding session.
            if diff_in_minutes < max_commit_diff_in_minutes:
                return diff_in_minutes / 60.0
            # The work of first commit of a session cannot be seen in git history,
            # so we make a blunt estimate of it
            return first_commit_addition_in_minutes / 60.0

        hours = [await estimate(a, b) for a, b in enumerate(commits_ts[:-1])]
        hours = sum(hours)
        ds.append([person, hours])
    df = pd.DataFrame(ds, columns=["author", "hours"])
    return df.sort_values(by="hours", ascending=False)


async def lines_of_code_changes_per_project(df):
    insertion_count = df["insertion"].sum()
    deletion_count = df["deletion"].sum()
    files_changed = df["filepath"].count()
    total_lines = insertion_count - deletion_count
    add_del_ratio = deletion_count / insertion_count
    return (
        files_changed,
        insertion_count,
        deletion_count,
        total_lines,
        add_del_ratio,
    )
