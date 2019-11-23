#!/usr/bin/env bash
aws s3 cp view/demo.html s3://arjun-demo
aws s3api put-object-acl --bucket arjun-demo --key demo.html --acl public-read
aws s3 cp view/dynamo_event.html s3://arjun-demo
aws s3api put-object-acl --bucket arjun-demo --key dynamo_event.html --acl public-read
