def add_labels_df(df):
    for index, row in df.iterrows():
        try:
            df.loc[index, 'labels'] = label_message(row['msg'])
        except Exception as e:
            df.loc[index, 'labels'] = '[Other]'

    return df


def label_message(msg):
    msg = msg.lower()
    labels = []

    bug_fix_keywords = ['bug', 'fix', 'error', 'patch', 'crash', 'debug', 'defect', 'issue', 'mistake', 'problem',
                        'resolve', 'repair', 'correct', 'fault', 'failure', 'troubleshoot', 'glitch', 'hitch', 'hotfix',
                        'resolve']
    enhancement_keywords = ['enhance', 'improve', 'optimize', 'refine', 'upgrade', 'streamline', 'boost', 'polish',
                            'revamp', 'augment', 'better', 'progress', 'advance', 'develop', 'modernize', 'innovate',
                            'strengthen', 'reinforce', 'amplify', 'perfect']
    new_feature_keywords = ['new', 'add', 'create', 'implement', 'introduce', 'develop', 'innovate', 'extend', 'expand',
                            'include', 'launch', 'build', 'generate', 'produce', 'propose', 'originate', 'initiate',
                            'establish', 'design', 'formulate']
    refactoring_keywords = ['refactor', 'clean', 'restructure', 'simplify', 'reorganize', 'modularize', 'streamline',
                            'tidy', 'optimize', 'rebuild', 'redesign', 'rewrite', 'rework', 'rearrange', 'consolidate',
                            'conservation', 'update', 'transform', 'reform', 'recondition']

    if any(keyword in msg for keyword in bug_fix_keywords):
        labels.append('Bug fixing')
    if any(keyword in msg for keyword in enhancement_keywords):
        labels.append('Enhancement')
    if any(keyword in msg for keyword in new_feature_keywords):
        labels.append('New feature')
    if any(keyword in msg for keyword in refactoring_keywords):
        labels.append('Refactoring')

    if len(labels) == 0:
        labels.append('Other')

    return labels
