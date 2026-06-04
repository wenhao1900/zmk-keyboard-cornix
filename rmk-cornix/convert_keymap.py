"""Convert cornix.vil to RMK keyboard.toml and vial.json."""
import json, re

# QMK → RMK keycode mapping
QMK_TO_RMK = {
    # Letters
    'KC_A': 'A','KC_B': 'B','KC_C': 'C','KC_D': 'D','KC_E': 'E','KC_F': 'F','KC_G': 'G',
    'KC_H': 'H','KC_I': 'I','KC_J': 'J','KC_K': 'K','KC_L': 'L','KC_M': 'M','KC_N': 'N',
    'KC_O': 'O','KC_P': 'P','KC_Q': 'Q','KC_R': 'R','KC_S': 'S','KC_T': 'T','KC_U': 'U',
    'KC_V': 'V','KC_W': 'W','KC_X': 'X','KC_Y': 'Y','KC_Z': 'Z',
    # Numbers (RMK uses Kc prefix)
    'KC_1': 'Kc1','KC_2': 'Kc2','KC_3': 'Kc3','KC_4': 'Kc4','KC_5': 'Kc5',
    'KC_6': 'Kc6','KC_7': 'Kc7','KC_8': 'Kc8','KC_9': 'Kc9','KC_0': 'Kc0',
    'KC_N1': 'Kc1','KC_N2': 'Kc2','KC_N3': 'Kc3','KC_N4': 'Kc4','KC_N5': 'Kc5',
    'KC_N6': 'Kc6','KC_N7': 'Kc7','KC_N8': 'Kc8','KC_N9': 'Kc9','KC_N0': 'Kc0',
    # Modifiers
    'KC_LCTRL': 'LCtrl','KC_LCTL': 'LCtrl',
    'KC_LSHIFT': 'LShift','KC_LSFT': 'LShift',
    'KC_LALT': 'LAlt','KC_LGUI': 'LGui',
    'KC_RCTRL': 'RCtrl','KC_RCTL': 'RCtrl',
    'KC_RSHIFT': 'RShift','KC_RSFT': 'RShift',
    'KC_RALT': 'RAlt','KC_RGUI': 'RGui',
    # Special
    'KC_ESCAPE': 'Escape','KC_ESC': 'Escape',
    'KC_TAB': 'Tab',
    'KC_CAPSLOCK': 'CapsLock','KC_CAPS': 'CapsLock',
    'KC_BSPACE': 'Backspace','KC_BSPC': 'Backspace',
    'KC_SPACE': 'Space','KC_SPC': 'Space',
    'KC_ENTER': 'Enter','KC_ENT': 'Enter','KC_RET': 'Enter',
    'KC_DELETE': 'Delete','KC_DEL': 'Delete',
    'KC_INSERT': 'Insert','KC_INS': 'Insert',
    'KC_HOME': 'Home','KC_END': 'End',
    'KC_PGUP': 'PageUp','KC_PGDN': 'PageDown',
    # Arrows
    'KC_UP': 'Up','KC_DOWN': 'Down','KC_LEFT': 'Left','KC_RIGHT': 'Right',
    # Symbols
    'KC_GRAVE': 'Grave','KC_GRV': 'Grave',
    'KC_MINUS': 'Minus','KC_MINS': 'Minus',
    'KC_EQUAL': 'Equal','KC_EQL': 'Equal',
    'KC_LBRACKET': 'LeftBracket','KC_LBRC': 'LeftBracket',
    'KC_RBRACKET': 'RightBracket','KC_RBRC': 'RightBracket',
    'KC_BSLASH': 'Backslash','KC_BSLS': 'Backslash',
    'KC_SCOLON': 'Semicolon','KC_SCLN': 'Semicolon','KC_SEMI': 'Semicolon',
    'KC_QUOTE': 'Quote','KC_QUOT': 'Quote','KC_SQT': 'Quote',
    'KC_COMMA': 'Comma','KC_COMM': 'Comma',
    'KC_DOT': 'Dot','KC_SLASH': 'Slash','KC_FSLH': 'Slash',
    # Function keys
    'KC_F1': 'F1','KC_F2': 'F2','KC_F3': 'F3','KC_F4': 'F4','KC_F5': 'F5','KC_F6': 'F6',
    'KC_F7': 'F7','KC_F8': 'F8','KC_F9': 'F9','KC_F10': 'F10','KC_F11': 'F11','KC_F12': 'F12',
    # Media
    'KC_VOLD': 'AudioVolDown','KC_VOLU': 'AudioVolUp','KC_MUTE': 'AudioMute',
    'KC_MPLY': 'MediaPlayPause','KC_MPRV': 'MediaPrevTrack','KC_MNXT': 'MediaNextTrack',
    # Mouse movement
    'KC_MS_U': 'MouseUp','KC_MS_D': 'MouseDown','KC_MS_L': 'MouseLeft','KC_MS_R': 'MouseRight',
    # Mouse scroll
    'KC_WH_U': 'MouseWheelUp','KC_WH_D': 'MouseWheelDown',
    'KC_WH_L': 'MouseWheelLeft','KC_WH_R': 'MouseWheelRight',
    # Mouse buttons
    'KC_BTN1': 'MouseBtn1','KC_BTN2': 'MouseBtn2','KC_BTN3': 'MouseBtn3',
    'KC_BTN4': 'MouseBtn4','KC_BTN5': 'MouseBtn5',
    # Keypad
    'KC_KP_0': 'Kp0','KC_KP_1': 'Kp1','KC_KP_2': 'Kp2','KC_KP_3': 'Kp3',
    'KC_KP_4': 'Kp4','KC_KP_5': 'Kp5','KC_KP_6': 'Kp6',
    'KC_KP_7': 'Kp7','KC_KP_8': 'Kp8','KC_KP_9': 'Kp9',
    'KC_KP_MINUS': 'KpMinus','KC_KP_PLUS': 'KpPlus',
    'KC_KP_SLASH': 'KpSlash','KC_KP_ASTERISK': 'KpAsterisk',
    'KC_KP_ENTER': 'KpEnter','KC_KP_DOT': 'KpDot',
    # Misc
    'KC_NO': '_','KC_TRNS': '_',
    'KC_NUMLOCK': 'NumLock','KC_SCROLLLOCK': 'ScrollLock',
    'KC_PSCREEN': 'PrintScreen','KC_PAUSE': 'Pause',
}

def convert_qmk_key(key):
    """Convert a QMK keycode string to RMK keycode string."""
    key = key.strip()
    if key == 'KC_NO':
        return '_'

    # Direct mapping
    if key in QMK_TO_RMK:
        return QMK_TO_RMK[key]

    # Layer/mod actions
    # MO(n) → MO(n)
    m = re.match(r'^MO\((\d+)\)$', key)
    if m: return f'MO({m.group(1)})'

    # TG(n) → TG(n)
    m = re.match(r'^TG\((\d+)\)$', key)
    if m: return f'TG({m.group(1)})'

    # TO(n) → TO(n)
    m = re.match(r'^TO\((\d+)\)$', key)
    if m: return f'TO({m.group(1)})'

    # LTn(KC_XXX) → LT(n, key)
    m = re.match(r'^LT(\d+)\((.+)\)$', key)
    if m:
        inner = convert_qmk_key(m.group(2))
        return f'LT({m.group(1)}, {inner})'

    # MOD_T(KC_XXX) → MT(key, modifier)
    # LALT_T, LGUI_T, LCTL_T, LSFT_T
    m = re.match(r'^(LALT|LGUI|LCTL|LSFT|RALT|RGUI|RCTL|RSFT)_T\((.+)\)$', key)
    if m:
        mod_map = {'LALT': 'LAlt', 'LGUI': 'LGui', 'LCTL': 'LCtrl', 'LSFT': 'LShift',
                    'RALT': 'RAlt', 'RGUI': 'RGui', 'RCTL': 'RCtrl', 'RSFT': 'RShift'}
        mod = mod_map[m.group(1)]
        inner = convert_qmk_key(m.group(2))
        return f'MT({inner}, {mod})'

    # MOD(KC_XXX) → WM(key, modifier)
    m = re.match(r'^(LALT|LGUI|LCTL|LSFT|RALT|RGUI|RCTL|RSFT)\((.+)\)$', key)
    if m:
        mod_map = {'LALT': 'LAlt', 'LGUI': 'LGui', 'LCTL': 'LCtrl', 'LSFT': 'LShift',
                    'RALT': 'RAlt', 'RGUI': 'RGui', 'RCTL': 'RCtrl', 'RSFT': 'RShift'}
        mod = mod_map[m.group(1)]
        inner = convert_qmk_key(m.group(2))
        return f'WM({inner}, {mod})'

    # User macros USER00 → MACRO(0)
    m = re.match(r'^USER(\d+)$', key)
    if m: return f'MACRO({int(m.group(1))})'

    # KC_ numbers without prefix
    m = re.match(r'^KC_(\d+)$', key)
    if m: return f'Kc{m.group(1)}'

    # Unknown - warn and use as-is
    print(f'  ⚠ Unknown keycode: {key}')
    return key


def main():
    with open('../cornix.vil') as f:
        vil = json.load(f)

    layers_data = vil['layout']
    num_layers = len(layers_data)

    # Build RMK keymap: 10 layers × 4 rows × 14 cols
    rmk_keymap = []
    for layer_idx in range(num_layers):
        layer = layers_data[layer_idx]
        # Initialize 4×14 matrix with "_" (transparent)
        matrix = [["_" for _ in range(14)] for _ in range(4)]

        for vial_row in range(8):
            vial_data = layer[vial_row]
            is_left = vial_row < 4
            phys_row = vial_row if is_left else vial_row - 4

            for vial_col in range(7):
                if vial_col >= len(vial_data):
                    break
                key = vial_data[vial_col]
                if key == -1:
                    continue  # sentinel, skip

                rmk_key = convert_qmk_key(str(key))

                if is_left:
                    phys_col = vial_col  # cols 0-6
                else:
                    # Right half: col 0→13, col 1→12, ..., col 5→8, col 6→7 (reversed?!)
                    # Actually from our analysis: .vil right half is in physical order
                    # .vil[4][0:6] maps to matrix[row][7:13]
                    phys_col = 7 + vial_col

                if 0 <= phys_row < 4 and 0 <= phys_col < 14:
                    matrix[phys_row][phys_col] = rmk_key

        rmk_keymap.append(matrix)

    # Generate keyboard.toml
    config = {
        'keyboard': {
            'name': 'cornix',
            'product_name': 'Cornix',
            'vendor_id': 0x4C4B,
            'product_id': 0x4643,
            'manufacturer': 'Cornix',
            'chip': 'nrf52840',
        },
        'layout': {
            'rows': 4,
            'cols': 14,
            'layers': num_layers,
            'keymap': rmk_keymap,
        },
        'ble': {'enabled': True},
        'split': {
            'connection': 'ble',
            'central': {
                'rows': 4,
                'cols': 7,
                'row_offset': 0,
                'col_offset': 0,
                'matrix': {
                    'row_pins': ['P0_30', 'P0_31', 'P0_29', 'P0_02'],
                    'col_pins': ['P0_28', 'P0_03', 'P1_10', 'P1_11', 'P1_13', 'P0_09', 'P0_10'],
                },
            },
            'peripheral': [{
                'rows': 4,
                'cols': 7,
                'row_offset': 0,
                'col_offset': 7,
                'matrix': {
                    'row_pins': ['P1_09', 'P0_28', 'P0_03', 'P1_10'],
                    'col_pins': ['P0_30', 'P0_31', 'P0_29', 'P0_02', 'P1_13', 'P0_10', 'P0_09'],
                },
            }],
        },
        'rmk': {
            'split_peripherals_num': 1,
        },
        'behavior': {},
    }

    # Write keyboard.toml manually (avoid toml lib dependency)
    with open('keyboard.toml', 'w') as f:
        f.write('# Cornix RMK Keyboard Configuration\n')
        f.write('# Auto-generated from cornix.vil\n\n')
        f.write('[keyboard]\n')
        f.write('name = "cornix"\n')
        f.write('product_name = "Cornix"\n')
        f.write('vendor_id = 0x4C4B\n')
        f.write('product_id = 0x4643\n')
        f.write('manufacturer = "Cornix"\n')
        f.write('chip = "nrf52840"\n\n')

        f.write('[layout]\n')
        f.write(f'rows = 4\n')
        f.write(f'cols = 14\n')
        f.write(f'layers = {num_layers}\n')

        # Write keymap array
        for layer_idx, matrix in enumerate(rmk_keymap):
            if layer_idx == 0:
                f.write('keymap = [\n')
            else:
                f.write(',\n')
            f.write('    [\n')
            for r, row in enumerate(matrix):
                keys_str = ', '.join(f'"{k}"' for k in row)
                if r < len(matrix) - 1:
                    f.write(f'        [{keys_str}],\n')
                else:
                    f.write(f'        [{keys_str}]\n')
            f.write('    ]')
        f.write('\n]\n\n')

        f.write('[ble]\n')
        f.write('enabled = true\n\n')

        f.write('[split]\n')
        f.write('connection = "ble"\n\n')

        f.write('[split.central]\n')
        f.write('rows = 4\n')
        f.write('cols = 7\n')
        f.write('row_offset = 0\n')
        f.write('col_offset = 0\n\n')

        f.write('[split.central.matrix]\n')
        f.write('row_pins = ["P0_30", "P0_31", "P0_29", "P0_02"]\n')
        f.write('col_pins = ["P0_28", "P0_03", "P1_10", "P1_11", "P1_13", "P0_09", "P0_10"]\n\n')

        f.write('[[split.peripheral]]\n')
        f.write('rows = 4\n')
        f.write('cols = 7\n')
        f.write('row_offset = 0\n')
        f.write('col_offset = 7\n\n')

        f.write('[split.peripheral.matrix]\n')
        f.write('row_pins = ["P1_09", "P0_28", "P0_03", "P1_10"]\n')
        f.write('col_pins = ["P0_30", "P0_31", "P0_29", "P0_02", "P1_13", "P0_10", "P0_09"]\n\n')

        f.write('[rmk]\n')
        f.write('split_peripherals_num = 1\n\n')

        f.write('[behavior]\n')

    # Verify keymap layers
    print(f'Generated {num_layers} layers, 4 rows × 14 cols')
    for i in range(num_layers):
        count = sum(1 for row in rmk_keymap[i] for k in row if k != '_')
        print(f'  Layer {i}: {count} active keys')

    # Generate vial.json
    vial_config = {
        'name': 'Cornix',
        'vendorId': '0x4C4B',
        'productId': '0x4643',
        'lighting': 'none',
        'matrix': {'rows': 4, 'cols': 14},
        'customKeycodes': [
            {'name': 'BT0', 'title': 'Bluetooth Channel 0', 'shortName': 'BT0'},
            {'name': 'BT1', 'title': 'Bluetooth Channel 1', 'shortName': 'BT1'},
            {'name': 'BT2', 'title': 'Bluetooth Channel 2', 'shortName': 'BT2'},
            {'name': 'NEXT_BT', 'title': 'Switch to next Bluetooth channel', 'shortName': 'Next\nBT'},
            {'name': 'PREV_BT', 'title': 'Switch to previous Bluetooth channel', 'shortName': 'Prev\nBT'},
            {'name': 'CLR_BT', 'title': 'Clear bond info for current channel', 'shortName': 'Clear\nBT'},
            {'name': 'SWITCH', 'title': 'Switch default output mode USB/BLE', 'shortName': 'Switch\nOutput'},
        ],
        'layouts': {
            'keymap': []
        }
    }

    # Generate vial layout grid (4 rows × 14 cols)
    for r in range(4):
        row = []
        for c in range(14):
            row.append(f'{r},{c}')
        vial_config['layouts']['keymap'].append(row)

    with open('vial.json', 'w') as f:
        json.dump(vial_config, f, indent=2)

    print('\n✅ keyboard.toml + vial.json generated!')
    print('\nLayer 5 (Mouse) right-hand keys:')
    for r in range(4):
        for c in range(7, 14):
            k = rmk_keymap[5][r][c]
            if k != '_':
                print(f'  row{r} col{c}: {k}')


if __name__ == '__main__':
    main()
