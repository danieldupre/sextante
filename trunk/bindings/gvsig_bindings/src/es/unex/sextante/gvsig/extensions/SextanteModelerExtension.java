package es.unex.sextante.gvsig.extensions;

import com.iver.andami.plugins.Extension;

import es.unex.sextante.gui.core.SextanteGUI;

public class SextanteModelerExtension
         extends
            Extension {


   public void initialize() {}


   public void execute(final String actionCommand) {

      SextanteGUI.getGUIFactory().showModelerDialog();

   }


   public boolean isEnabled() {

      return true;

   }


   public boolean isVisible() {

      return true;

   }

}
