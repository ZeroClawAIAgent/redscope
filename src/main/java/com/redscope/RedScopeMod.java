package com.redscope;

import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * RedScope - A redstone debugger and visualizer for Minecraft.
 * 
 * This is a minimal working version for Minecraft 26.1.2 (unobfuscated).
 * Full features (mixins, rendering, game tests) will be added in future updates.
 */
public class RedScopeMod implements ModInitializer {
    public static final String MOD_ID = "redscope";
    public static final String MOD_NAME = "RedScope";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        LOGGER.info("RedScope initialized!");
        LOGGER.info("Redstone debugger and visualizer for Minecraft 26.1.2");
        
        // TODO: Initialize core components
        // - Redstone signal tracking
        // - Circuit analysis
        // - Visual overlay rendering
    }
}