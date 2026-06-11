package com.redscope.model;

import java.util.Map;

public record RedstoneSnapshot(int tick, Map<net.minecraft.core.BlockPos, ComponentState> states) {
}
