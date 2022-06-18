#!/usr/bin/env python3
# sndslib by @undersfx


class Presenter:
    def summary(self, summary, blocked_ips):
        message = (
            f"Date: {summary['date']:>9} \n"
            f"IPs: {summary['ips']:>10} \n"
            f"Green: {summary['green']:>8} \n"
            f"Yellow: {summary['yellow']:>7} \n"
            f"Red: {summary['red']:>10} \n"
            f"Trap Hits: {summary['traps']:>4} \n"
            f"Blocked: {len(blocked_ips):>6}"
        )

        print(message)

    def ip_data(self, ipdata):
        message = (
            f"Activity: {ipdata['activity_start']} until {ipdata['activity_end']} \n"
            f"IP: {ipdata['ip_address']:>15} \n"
            f"Messages: {ipdata['message_recipients']:>9} \n"
            f"Filter: {ipdata['filter_result']:>11} \n"
            f"Complaint: {ipdata['complaint_rate']:>8} \n"
            f"Trap Hits: {ipdata['traphits']:>8} \n"
        )

        print(message)

    def list_blocked_ips(self, blocked_ips):
        print('\n'.join(blocked_ips))

    def list_blocked_ips_rdns(self, blocked_ips_rdns):
        for ip in blocked_ips_rdns:
            print(ip['ip'] + ';' + ip['rdns'])
