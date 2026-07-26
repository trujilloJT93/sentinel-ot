package io.sentinelot;

import io.sentinelot.domain.Asset;
import io.sentinelot.domain.AssetIdentity;

public class Main {
    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" 🚨 INICIANDO ENGINE DE SENTINEL OT...");
        System.out.println("==================================================\n");

        // 1. Generamos un ID único para un activo industrial
        AssetIdentity idActivo = AssetIdentity.generate();

        // 2. Creamos un activo real (por ejemplo, un PLC de subestación eléctrica)
        Asset plcSubestacion = new Asset(idActivo, "PLC Siemens S7-1500 (Subestación Central)", "192.168.10.45");

        // 3. Imprimimos sus datos por consola
        System.out.println("[+] Activo creado exitosamente:");
        System.out.println("    • ID Unico : " + plcSubestacion.getId());
        System.out.println("    • Nombre   : " + plcSubestacion.getName());
        System.out.println("    • IP OT    : " + plcSubestacion.getIpAddress());

        System.out.println("\n==================================================");
        System.out.println(" [OK] Dominio validado e instanciado con éxito.");
        System.out.println("==================================================");
    }
}