import ipaddress
import pprint
import boto3

client = boto3.client("ec2")

subnets = client.describe_subnets(Filters=[{"Name": "vpc-id", "Values": ["vpc-XXXXX"]}])

nets = [ipaddress.ip_network(i["CidrBlock"]) for i in subnets["Subnets"]]

vpc = ipaddress.ip_network("10.4.0.0/16")

excluded_subnets = list(vpc.address_exclude(nets[0]))

for net in nets:
    for i in excluded_subnets:
        if i.overlaps(net):
            excluded_subnets.remove(i)
            excluded_subnets.extend(list(i.address_exclude(net)))

pprint.pprint(
    [str(i) for i in sorted(excluded_subnets, reverse=True, key=lambda r: len(list(r.hosts())))]
)

output = [
    "10.4.32.0/19",
    "10.4.128.0/20",
    "10.4.240.0/20",
    "10.4.8.0/21",
    "10.4.72.0/21",
    "10.4.88.0/21",
    "10.4.232.0/21",
]
