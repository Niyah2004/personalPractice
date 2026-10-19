# ARN format cheat sheet

`arn:partition:service:region:account-id:resource`

| Part       | Example          | Notes                                              |
|------------|------------------|----------------------------------------------------|
| partition  | `aws`            | `aws-cn`, `aws-us-gov` for China / GovCloud        |
| service    | `lambda`         | service namespace                                  |
| region     | `us-east-1`      | empty for global services (IAM, S3 buckets)        |
| account-id | `123456789012`   | 12 digits; empty for S3 buckets                    |
| resource   | `function:my-fn` | may contain `:` or `/`, e.g. `role/Admin`          |
