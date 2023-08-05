import json

def build_disco_profile(args):
    if args.recurrence == 'NONE':
        return False

    schedule = {}

    if args.recurrence == 'WEEKLY':
        schedule['patternType'] = 'WEEKLY'
        schedule['pattern'] = args.daysofweek.lower()
        schedule['startTime'] = args.starthour
    elif args.recurrence == 'DAILY':
        schedule['patternType'] = 'DAILY'
        schedule['pattern'] = 1
        schedule['startTime'] = args.starthour

    discoprofile = [
            {
                "policy": {
                    "name": args.azname,
                    "entityType": "ALL",
                    "matchType": "ANY",
                    "rules": [
                        {
                        "filterType": "ANY_CLOUD_RESOURCE"
                        }
                    ],
                    "actions": [
                        {
                        "action": "MANAGE DEVICE"
                        }
                    ]
                },
                "scanNow": True,
                "schedule": schedule,              
            }
        ]
    return discoprofile

def do_add_azure_arm(ops, args):
    obj = {
            "displayName": args.azname,
            "credential": {
                "credentialType": "AZURE",
                "SubscriptionId": args.azsub,
                "AzureType": "ARM",
                "TenantId": args.aztenant,
                "ClientID": args.azclient,
                "SecretKey": args.azsecret
             }
    }
    discoprofile = build_disco_profile(args)
    if discoprofile:
        obj['discoveryProfiles'] = discoprofile
    return ops.add_integration("Azure", obj)

def do_add_azure_asm(ops, args):
    obj = {
            "displayName": args.azname,
            "credential": {
                "credentialType": "AZURE",
                "SubscriptionId": args.azsub,
                "AzureType": "ASM",
                "ManagementCertificate": args.azcert,
                "KeystorePassword": args.azkspw
             }
    }
    discoprofile = build_disco_profile(args)
    if discoprofile:
        obj['discoveryProfiles'] = discoprofile
    return ops.add_integration("Azure", obj)