package com.redscope.render;

import net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;

import java.util.List;

public final class OverlayRenderer {
    private OverlayRenderer() {}

    public static void register() {
        WorldRenderEvents.END.register((context) -> {
            // TODO: Render per-component overlay using com.redscope.core.RedstoneReader.
        });
    }
}
