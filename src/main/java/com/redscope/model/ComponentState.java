package com.redscope.model;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Block;

public record ComponentState(BlockPos pos, Block block, int powerLevel, int delay, boolean locked, String mode) {
}
