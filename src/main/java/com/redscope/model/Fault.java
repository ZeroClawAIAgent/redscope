package com.redscope.model;

import net.minecraft.core.BlockPos;

public record Fault(BlockPos pos, String type, String message, Severity severity) {
    public enum Severity {
        INFO, WARNING, ERROR
    }
}
