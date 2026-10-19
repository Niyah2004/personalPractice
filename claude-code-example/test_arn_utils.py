import unittest

from arn_utils import extract_region, is_valid_access_key_id, parse_arn


class ParseArnTest(unittest.TestCase):
    def test_lambda_arn(self):
        parts = parse_arn("arn:aws:lambda:us-east-1:123456789012:function:my-fn")
        self.assertEqual(parts["service"], "lambda")
        self.assertEqual(parts["account"], "123456789012")
        self.assertEqual(parts["resource"], "function:my-fn")

    def test_invalid_arn_raises(self):
        with self.assertRaises(ValueError):
            parse_arn("not-an-arn")


class ExtractRegionTest(unittest.TestCase):
    def test_regional_arn(self):
        self.assertEqual(extract_region("arn:aws:sqs:eu-west-2:123456789012:queue"), "eu-west-2")

    def test_global_arn_has_no_region(self):
        self.assertIsNone(extract_region("arn:aws:s3:::my-bucket"))


class AccessKeyIdTest(unittest.TestCase):
    def test_aws_documented_example_key(self):
        self.assertTrue(is_valid_access_key_id("AKIAIOSFODNN7EXAMPLE"))

    def test_wrong_prefix(self):
        self.assertFalse(is_valid_access_key_id("ASIAIOSFODNN7EXAMPLE"))


if __name__ == "__main__":
    unittest.main()
