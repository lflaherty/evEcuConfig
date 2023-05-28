# ECU Config CLI Tool

## Files

### Executables

| File | Description |
| ---- | ----------- |
| `log_view.py` | Continuously prints all received log data on serial (message ID 0x02). |
| `debug_term.py` | Prints all log and debug log messages (IDs 0x02 and 0x09). Text input to script is transmitted as a debug message to ECU (msg 0x09). |
| `mock_log_view.py` | Variant of `log_view.py` that mocks the hardware serial. Used for testing/script development |
| `cmd_sdc.py` (Deprecated) | Run a Set SDC (shutdown circuit) test command (message ID 0x101) |
| `cmd_pdm.py` (Deprecated) | Run a Set PDM (power distribution module) test command (message ID 0x102) |

### Libraries/helpers

| File | Description |
| ---- | ----------- |
| `decode_common.py` | Serial bus message frame decoder. |
| `encode_common.py` | Serial bus message frame encoder. |
| `serial_common.py` | Serial bus handlers. Helps passing data to decoder. |
| `serial_mock.py` | Mock version of `serial_common.py`. Implements similar functionality but doesn't communicate with real serial bus. |
| `colors.py` | Helper to store diffent terminal color codes. |
