# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from structured_log_json import jsonlogger
import logging
'''
1. inherited  logging class Formatter;
2. inherited  logging class Handler;
'''

'''
test :
{
	"event_header": [
		"V.1.1.1-01",
		"2021-11-22 17:50:51,520",
		"INFO",
		"line_id:248",
		"stat",
		"0000"
	],
	"event_entity":
	{
        "event_domain":"mimic_multimode_ruling",
        "event_action":"multimode_ruling",
        "object":"router_table",
        "service":"multimode_ruling_router_item",
        "status":"",
        "subject":"",
        "router_multimode_ruling":
		[
            {
                "exception_type":"missing_router_item",
                "action":"del_route",
	            "executor_role":"master",
                "prefix":"2.2.2.2",
                "mask":32,
                "nexthop_info.nexthop":["100.0.13.3"],
                "nexthop_info.ifname":["GigEth0"],
                "nexthop_info.label":[]
            }
			 
		]
	}
}
'''


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    logger = jsonlogger.setup_logging("./", "mimicrouter", __name__, "dmf", logging.INFO,['filename','processName'])
    test = {

        "event_domain": "mimic_multimode_ruling",
        "event_action": "attack",
        "router_multimode_ruling":
            [
	            {
                    "exception_type":"missing_router_item",
                    "action":"del_route",
                    "executor_role":"master",
                    "prefix":"2.2.2.2",
                    "mask":32,
                    "nexthop_info.nexthop":["100.0.13.3"],
                    "nexthop_info.ifname":["GigEth0"],
                    "nexthop_info.label":[]
                },
                {
                    "exception_type":"missing_router_item",
                    "action":"del_route",
                    "executor_role":"master",
                    "prefix":"11.11.11.11",
                    "mask":32,
                    "nexthop_info.nexthop":["100.0.13.3"],
                    "nexthop_info.ifname":["GigEth0"],
                    "nexthop_info.label":[]
                },
                {
                    "exception_type":"missing_router_item",
                    "action":"del_route",
                    "executor_role":"master",
                    "prefix":"100.0.12.0",
                    "mask":24,
                    "nexthop_info.nexthop":["100.0.13.3"],
                    "nexthop_info.ifname":["GigEth0"],
                    "nexthop_info.label":[]
                },
	            {
                    "exception_type":"missing_router_item",
                    "action":"del_route",
                    "executor_role":"master",
                    "prefix":"100.0.17.0",
                    "mask":24,
                    "nexthop_info.nexthop":["100.0.13.3"]
			    }

		    ]
    }
    for i in range(5):
        logger.info("test",extra=test)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
