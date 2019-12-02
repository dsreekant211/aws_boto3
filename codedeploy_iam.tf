resource "aws_iam_instance_profile" "code_deploy" {
  name = "code_deploy"
  role = "${aws_iam_role.codedeploy_role.name}"
}


resource "aws_iam_role" "codedeploy_role" {
  name = "codedeploy_role"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "codedeploy.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}
// source "aws_iam_policy" "ec2_codedeploy" {
//   name        = "ec2_codedeploy"
//   path        = "/"
//   description = "My test policy"

//   policy = <<EOF
// {
//     "Version": "2012-10-17",
//     "Statement": [
//         {
//             "Action": [
//                 "s3:Get*",
//                 "s3:List*"
//             ],
//             "Effect": "Allow",
//             "Resource": "*"
//         }
//     ]
// }
// EOF
// }
resource "aws_iam_policy_attachment" "test-attach" {
  name       = "test-attachment"
//   users      = ["${aws_iam_user.user.name}"]
  roles      = ["${aws_iam_role.codedeploy_role.name}"]
//   groups     = ["${aws_iam_group.group.name}"]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole"
}