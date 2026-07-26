package io.sentinelot.domain;

import java.util.Objects;

/**
 * Representa un Activo Industrial dentro de la red OT de Sentinel OT.
 */
public class Asset {

    private final AssetIdentity id;
    private final String name;
    private final String ipAddress;

    public Asset(AssetIdentity id, String name, String ipAddress) {
        if (id == null) {
            throw new IllegalArgumentException("El activo debe tener una identidad válida.");
        }
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("El nombre del activo no puede estar vacío.");
        }
        if (ipAddress == null || ipAddress.trim().isEmpty()) {
            throw new IllegalArgumentException("La dirección IP no puede estar vacía.");
        }

        this.id = id;
        this.name = name.trim();
        this.ipAddress = ipAddress.trim();
    }

    public AssetIdentity getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getIpAddress() {
        return ipAddress;
    }

    @Override
    public boolean equals(Object o) {
        if (this.id == null) return false;
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Asset asset = (Asset) o;
        return Objects.equals(id, asset.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}