package com.redscope.mixin;

import net.minecraft.level.Level;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.api.mixin.Mixin;
import org.spongepowered.api.mixin.injection.At;
import org.spongepowered.api.mixin.injection.Inject;
import org.spongepowered.api.mixin.injection.callback.CallbackInfo;

@Mixin(Level.class)
public class BlockUpdateMixin {
    @Inject(method = "onBlockStateChange", at = @At("HEAD"))
    private void onBlockUpdate(BlockPos pos, BlockState oldState, BlockState newState, CallbackInfo ci) {
        // Block update hook for live refresh will be implemented here
    }
}
