package com.redscope.model;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Block;

public record RedstoneComponent(BlockPos pos, Block block, int powerLevel) {
}
