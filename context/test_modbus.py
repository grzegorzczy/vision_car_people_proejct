# -*- coding: utf-8 -*-
"""
test_modbus.py — samodzielny test lacza Modbus TCP ze sterownikiem (Faza 3).

Zapisuje kilka zestawow wartosci do HR0..2 i ODCZYTUJE je z powrotem,
by potwierdzic, ze polaczenie i mapowanie rejestrow dzialaja.

Uruchomienie (podaj IP swojego variTRON, jesli inne niz w config.py):
    python test_modbus.py --host 192.168.0.10
    python test_modbus.py                      # uzyje config.MODBUS_HOST
"""

import argparse
import time

from pymodbus.client import ModbusTcpClient

from vision import config


def main():
    ap = argparse.ArgumentParser(description="Test lacza Modbus TCP ze sterownikiem")
    ap.add_argument("--host", default=config.MODBUS_HOST, help="192.168.10.248")
    ap.add_argument("--port", type=int, default=config.MODBUS_PORT)
    ap.add_argument("--unit", type=int, default=config.MODBUS_UNIT_ID, help="device_id")
    args = ap.parse_args()

    print("=" * 60)
    print(f" TEST MODBUS -> {args.host}:{args.port} (device_id={args.unit})")
    print("=" * 60)

    client = ModbusTcpClient(args.host, port=args.port, timeout=2)
    if not client.connect():
        print(f"[FAIL] Nie moge polaczyc sie z {args.host}:{args.port}")
        print("       Sprawdz: IP, czy sterownik online, firewall, port 502.")
        return
    print("[ OK ] Polaczono ze sterownikiem.")

    # (object_code, confidence 0..100, detection_count)
    tests = [
        (4, 79, 3),   # telefon, 79%, 3 detekcje  -> SILOWNIK 2
        (6, 88, 1),   # klawiatura, 88%           -> SILOWNIK 1
        (1, 90, 1),   # butelka, 90%              -> PRZEPUSC
        (0, 0, 0),    # brak
    ]

    ok_all = True
    for values in tests:
        w = client.write_registers(config.REG_OBJECT_CODE, list(values), device_id=args.unit)
        if w.isError():
            print(f"[FAIL] Zapis {values}: {w}")
            ok_all = False
            continue
        r = client.read_holding_registers(config.REG_OBJECT_CODE, count=3, device_id=args.unit)
        readback = r.registers if not r.isError() else None
        match = "OK" if readback == list(values) else "ROZNICA!"
        print(f"[ {('OK ' if match=='OK' else 'FAIL')}] zapis {list(values)} | odczyt {readback}  [{match}]")
        ok_all = ok_all and (match == "OK")
        time.sleep(0.5)

    client.close()
    print("-" * 60)
    print("[ OK ] Test zakonczony." if ok_all else "[WARN] Sa rozbieznosci — sprawdz konfiguracje serwera Modbus.")
    print("=" * 60)


if __name__ == "__main__":
    main()
