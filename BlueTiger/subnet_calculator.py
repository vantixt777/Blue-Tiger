def subnet_calculator(ip_address, subnet_mask):
    """
    Calculates subnet information based on an IP address and subnet mask.

    Args:
        ip_address (str): The IP address in dotted decimal notation (e.g., "192.168.1.10").
        subnet_mask (str): The subnet mask in dotted decimal notation (e.g., "255.255.255.0").

    Returns:
        dict: A dictionary containing the network address, broadcast address,
              first usable host, last usable host, and total number of hosts.
              Returns None if the input is invalid.
    """
    try:
        def ip_to_binary(ip):
            return ''.join([format(int(x), '08b') for x in ip.split('.')])

        def binary_to_ip(binary_ip):
            octets = [binary_ip[i:i+8] for i in range(0, 32, 8)]
            return '.'.join([str(int(octet, 2)) for octet in octets])

        ip_binary = ip_to_binary(ip_address)
        mask_binary = ip_to_binary(subnet_mask)

        if len(ip_binary) != 32 or len(mask_binary) != 32:
            return None

        # Calculate network address
        network_binary = ''.join([str(int(ip_bit) & int(mask_bit)) for ip_bit, mask_bit in zip(ip_binary, mask_binary)])
        network_address = binary_to_ip(network_binary)

        # Calculate broadcast address
        broadcast_binary = ''.join([str(int(ip_bit) | (int(mask_bit) ^ 1)) for ip_bit, mask_bit in zip(ip_binary, mask_binary)])
        broadcast_address = binary_to_ip(broadcast_binary)

        # Calculate usable host range
        host_bits = mask_binary.count('0')
        total_hosts = 2**host_bits
        usable_hosts = total_hosts - 2 if total_hosts > 1 else 0

        if usable_hosts > 0:
            first_usable_binary = list(network_binary)
            first_usable_binary[-host_bits:] = ['0'] * (host_bits - 1) + ['1']
            first_usable_host = binary_to_ip("".join(first_usable_binary))

            last_usable_binary = list(broadcast_binary)
            last_usable_binary[-host_bits:] = ['1'] * (host_bits - 1) + ['0']
            last_usable_host = binary_to_ip("".join(last_usable_binary))
        else:
            first_usable_host = "N/A"
            last_usable_host = "N/A"

        return {
            "Network Address": network_address,
            "Broadcast Address": broadcast_address,
            "First Usable Host": first_usable_host,
            "Last Usable Host": last_usable_host,
            "Total Hosts": total_hosts,
            "Usable Hosts": usable_hosts
        }

    except ValueError:
        return None

if __name__ == "__main__":
    banner = r"""
  ⠀           (\ __ /)
              (UwU)
       ＿ノ ヽ ノ＼＿ 
    /　`/ ⌒Ｙ⌒ Ｙ　 \
 ( 　(三ヽ人　 /　 　|
|　ﾉ⌒＼ ￣￣ヽ　 ノ
ヽ＿＿＿＞､＿＿／
          ｜( 王 ﾉ〈 
           /ﾐ`ー―彡\ 
    """
    print(banner)
    print("------------------------------------")

    ip = input("Enter IP Address (e.g., 192.168.1.10): ")
    mask = input("Enter Subnet Mask (e.g., 255.255.255.0): ")

    result = subnet_calculator(ip, mask)

    if result:
        print("\nSubnet Calculation Results:")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("Invalid IP Address or Subnet Mask format.")