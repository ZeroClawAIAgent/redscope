package com.redscope.config;

import com.terraformersmc.modmenu.api.ConfigScreenFactory;
import com.terraformersmc.modmenu.api.ModMenuApi;
import me.shedaniel.cloth.config2.api.ConfigBuilder;
import me.shedaniel.clothconfig2.api.ConfigEntryBuilder;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

public class ModMenuIntegration implements ModMenuApi {
    @Override
    public ConfigScreenFactory<?> getModConfigScreenFactory() {
        return parent -> {
            ConfigBuilder builder = ConfigBuilder.create()
                    .setParentScreen(parent)
                    .setTitle(Component.translatable("config.redscope.title"));

            ConfigEntryBuilder entryBuilder = builder.entryBuilder();

            builder.getOrCreateCategory(Component.translatable("config.redscope.general"))
                    .addEntry(entryBuilder.startIntSlider(Component.translatable("config.redscope.visualization_radius"), RedScopeConfig.visualizationRadius, 8, 128)
                            .setDefaultValue(32)
                            .setSaveConsumer(value -> RedScopeConfig.visualizationRadius = value)
                            .build());

            return builder.build();
        };
    }
}
