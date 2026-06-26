export const querySpaceReviewCopy = {
  title: 'Query Space Review',
  subtitle: 'Review generated clusters, priorities, dedupe status, and citation-likelihood signals before running an audit.',
  lowSampleNote: 'Small query sets are directional; expand coverage before making stable conclusions.',
};

export const queryReviewActions = [
  'Approve query',
  'Edit query',
  'Reject duplicate',
  'Boost priority',
  'Lower priority',
];

export const queryReviewColumns = [
  'Query',
  'Cluster',
  'Perspective',
  'Citation likelihood',
  'Business value',
  'Priority score',
  'Dedupe status',
];
