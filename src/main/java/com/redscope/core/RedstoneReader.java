package com.redscope.core;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;

public final class RedstoneReader {

    private RedstoneReader() {}

    public static int getReceivedPower(Level level, BlockPos pos) {
        return level.getReceivedRedstonePower(pos);
    }

    public static int getStrongPower(Level level, BlockPos pos) {
        return level.getStrongRedstonePower(pos);
    }

    public static boolean isReceivingPower(Level level, BlockPos pos) {
        return level.isReceivingRedstonePower(pos);
    }

    public static int getPower(Level level, BlockPos pos) {
        BlockState state = level.getBlockState(pos);
        return state.getSignal(level, pos, net.minecraft.world.level.block.state.properties.BlockStateProperties.REDSTONE_SIGNAL);
    }
}
