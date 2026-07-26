package io.sentinelot.domain;

import java.util.Objects;
import java.util.UUID;

/**
 * Representa el identificador único e inmutable de un Activo Industrial.
 */
public final class AssetIdentity {

    private final String value;

    private AssetIdentity(String value) {
        if (value == null || value.trim().isEmpty()) {
            throw new IllegalArgumentException("El ID del activo no puede estar vacío.");
        }
        this.value = value.trim();
    }

    public static AssetIdentity generate() {
        return new AssetIdentity(UUID.randomUUID().toString());
    }

    public static AssetIdentity of(String value) {
        return new AssetIdentity(value);
    }

    public String getValue() {
        return value;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AssetIdentity that = (AssetIdentity) o;
        return Objects.equals(value, that.value);
    }

    @Override
    public int hashCode() {
        return Objects.hash(value);
    }

    @Override
    public String toString() {
        return value;
    }
}