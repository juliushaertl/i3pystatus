from i3pystatus import IntervalModule
from i3pystatus.core.command import run_through_shell

__author__ = 'facetoe'


class OpenVPN(IntervalModule):
    """
    Monitor OpenVPN connections.
    Currently only supports systems that use Systemd.

    Formatters:

    * {vpn_name} — Same as setting.
    * {status} — Unicode up or down symbol.
    * {output} — Output of status_command.
    * {label} — Label for this connection, if defined.

    """

    colour_up = "#00ff00"
    colour_down = "#FF0000"
    status_up = '▲'
    status_down = '▼'
    format = "{vpn_name} {status}"
    status_command = "bash -c \"systemctl show openvpn@%(vpn_name)s | grep -oP 'ActiveState=\K(\w+)'\""

    label = ''
    vpn_name = ''

    settings = (
        ("format", "Format string"),
        ("colour_up", "VPN is up"),
        ("colour_down", "VPN is down"),
        ("status_down", "Symbol to display when down"),
        ("status_up", "Symbol to display when up"),
        ("vpn_name", "Name of VPN"),
    )

    def init(self):
        if not self.vpn_name:
            raise Exception("vpn_name is required")

    def run(self):
        command_result = run_through_shell(self.status_command % {'vpn_name': self.vpn_name}, enable_shell=True)
        output = command_result.out.strip()

        if output == 'active':
            color = self.colour_up
            status = self.status_up
        else:
            color = self.colour_down
            status = self.status_down

        vpn_name = self.vpn_name
        label = self.label

        self.data = locals()
        self.output = {
            "full_text": self.format.format(**locals()),
            'color': color,
        }
