from .merge_conflict import *

scenario_hook = {
    "merge_conflict": setup_merge_conflict,
    "check_branch_created": check_branch_created,
    "check_commit_with_fix": check_commit_with_fix,
    "check_merge_attempted": check_merge_attempted,
    "check_conflict_resolved": check_conflict_resolved
}