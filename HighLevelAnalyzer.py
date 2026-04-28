from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting

# Register Map Names (Extracted from Table 7-1)
REGISTER_MAP = {
    0x00: "NOP", 0x01: "COMMON_STATUS", 0x02: "COMMON_CFG", 0x03: "INTERFACE_CFG",
    0x04: "GPIO_CFG", 0x05: "ALERT_CFG0", 0x06: "ALERT_CFG1", 0x07: "ALERT_CFG2",
    0x08: "ALERT_STATUS", 0x10: "DRV_CFG0", 0x11: "DRV_CFG1", 0x12: "DRV_REF",
    0x20: "SENSE_CONFIG0", 0x21: "SENSE_CONFIG1", 0x22: "SENSE_CONFIG2",
    0x23: "ADC_CFG", 0x24: "FILTER_CFG", 0x25: "FILTER_DATA", 0x26: "ADC_DATA",
    0x43: "SRAM_CFG", 0x44: "SRAM_DATA"
}

class AFE63MA1Decoder(HighLevelAnalyzer):
    result_types = {
        'afe_frame': { 'format': '{{data.op}} {{data.address}}: {{data.value}}' }
    }

    def __init__(self):
        pass

    def decode(self, frame: AnalyzerFrame):
        # AFE63MA1 uses 24-bit frames [cite: 1059]
        raw_data = frame.data['mosi'] # or 'miso' for read response
        
        # Extract bits based on Figure 6-9 and Table 6-4 [cite: 1069, 1074]
        rw_bit = (raw_data >> 23) & 0x01
        addr = (raw_data >> 16) & 0x7F
        data_val = raw_data & 0xFFFF

        op_name = "READ" if rw_bit == 1 else "WRITE" [cite: 1069]
        reg_name = REGISTER_MAP.get(addr, f"REG_{addr:02X}")

        return AnalyzerFrame('afe_frame', frame.start_time, frame.end_time, {
            'op': op_name,
            'address': reg_name,
            'value': f'0x{data_val:04X}'
        })