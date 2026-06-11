package com.redscope.mixin;

import net.minecraft.server.level.ServerLevel;
import org.spongepowered.api.mixin.Mixin;
import org.spongepowered.api.mixin.injection.At;
import org.spongepowered.api.mixin.injection.Inject;
import org.spongepowered.api.mixin.injection.callback.CallbackInfo;

@Mixin(ServerLevel.class)
public class WorldTickMixin {
    @Inject(method = "tick", at = @At("HEAD"))
    private void onTick(CallbackInfo ci) {
        // Timeline recording hook will be implemented here
    }
}
