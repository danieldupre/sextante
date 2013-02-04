

package es.unex.sextante.gui.modeler;

import info.clearthought.layout.TableLayout;
import info.clearthought.layout.TableLayoutConstants;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseListener;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

import javax.swing.AbstractAction;
import javax.swing.ComboBoxModel;
import javax.swing.DefaultComboBoxModel;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JFileChooser;
import javax.swing.JLabel;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JScrollPane;
import javax.swing.JSeparator;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.JSpinner;
import javax.swing.JCheckBox;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingConstants;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.text.JTextComponent;
import javax.swing.tree.DefaultMutableTreeNode;

import es.unex.sextante.core.GeoAlgorithm;
import es.unex.sextante.core.ObjectAndDescription;
import es.unex.sextante.core.OutputObjectsSet;
import es.unex.sextante.core.Sextante;
import es.unex.sextante.gui.algorithm.GenericFileFilter;
import es.unex.sextante.gui.core.SextanteGUI;
import es.unex.sextante.gui.modeler.parameters.ParameterPanel;
import es.unex.sextante.gui.settings.SextanteModelerSettings;
import es.unex.sextante.outputs.Output;


public class ModelerPanel
extends
JPanel {

	private JPanel          jModelPanel;
	private JPanel          jElementsPanel;
	private JButton         jButtonMenu;
	private JButton         jButtonEdit = null;
	private JButton         jButtonDelete = null;
	private JPopupMenu		popup;
	private JMenuItem		jMenuSave;
	private JButton         jButtonHelp;
	private JPanel          jPanelButtonsModel;
	private JTextField      jTextFieldName;
	private JComboBox       jComboBoxGroup;
	private JLabel          jLabelGroup;
	private JLabel          jLabelName;
	private JScrollPane     jModelGraphicalDescriptionPanel;
	private JTabbedPane     jElementsTabbedPane;
	private JButton         jButtonAdd;
	private JPanel          jPanelButtonsElements;
	private InputsPanel     inputsPanel;
	private AlgorithmsPanel extensionsPanel;
	private JSplitPane      jSplitPane;
	private ModelGraphPanel modelGraphPanel;
	private JCheckBox		jGridBox;
	private JSpinner      	jGridSize;
	private JButton			jScaleButtonMinus;
	private JButton			jScaleButtonOne;
	private JButton			jScaleButtonPlus;
	
	
	private ObjectAndDescription	currentNode = null;
	private double			dGridSize = 10.0;
	private double			dScale = 1.0;

	private ModelAlgorithm  m_Algorithm;
	private final HashMap   m_DataObjects;                  //all data objects, whether generated by modules or as input from the user
	private final ArrayList m_InputKeys;                    //keys of those elements in m_DataObjects that come from user input
	private boolean         m_bHasChanged;

	private final JDialog   m_Parent;


	public ModelerPanel(final JDialog parent) {

		m_DataObjects = new HashMap();
		m_InputKeys = new ArrayList();
		m_Algorithm = new ModelAlgorithm();
		m_Parent = parent;

		initGUI();

		newModel();

	}


	private void initGUI() {
		{
			final BorderLayout thisLayout = new BorderLayout();
			this.setLayout(thisLayout);
			this.setSize(new java.awt.Dimension(950, 630));
			jMenuSave= new JMenuItem(new AbstractAction(Sextante.getText("Save")) {
	            public void actionPerformed(ActionEvent e) {
	            	saveModel(false);
	            }
	        });
			{
				jSplitPane = new JSplitPane();
				this.add(jSplitPane, BorderLayout.CENTER);
				{
					jModelPanel = new JPanel();
					final TableLayout jModelPanelLayout = new TableLayout(new double[][] {
							{ 	5.0, 
								TableLayoutConstants.MINIMUM,
								TableLayoutConstants.FILL,
								TableLayoutConstants.MINIMUM,
								TableLayoutConstants.FILL,
								5.0 },
								{ 7.0, TableLayoutConstants.MINIMUM, TableLayoutConstants.FILL, 5.0, 30.0, 5.0 } });
					jModelPanelLayout.setHGap(5);
					jModelPanelLayout.setVGap(5);
					jModelPanel.setLayout(jModelPanelLayout);
					jSplitPane.add(jModelPanel, JSplitPane.RIGHT);

					modelGraphPanel = new ModelGraphPanel(m_Algorithm, m_DataObjects, m_InputKeys, this, m_Parent);
					jModelGraphicalDescriptionPanel = new JScrollPane();
					jModelGraphicalDescriptionPanel.setViewportView(modelGraphPanel);
					jModelGraphicalDescriptionPanel.setWheelScrollingEnabled(false);
										
					modelGraphPanel.setPreferredSize(new java.awt.Dimension(580, 401));
					{
						jLabelName = new JLabel();						
						jLabelName.setText(Sextante.getText("Name")+":");
						jModelPanel.add(jLabelName, "1, 1");
					}					
					{
						jTextFieldName = new JTextField();						
						jTextFieldName.addFocusListener(new FocusAdapter() {
							@Override
							public void focusLost(final FocusEvent e) {
								m_bHasChanged = true;
								m_Algorithm.setName(jTextFieldName.getText());
							}
						});
						jModelPanel.add(jTextFieldName, "2, 1");
					}
					{
						jLabelGroup = new JLabel();						
						jLabelGroup.setText(Sextante.getText("Group"+":"));
						jModelPanel.add(jLabelGroup, "3, 1");
					}
					{
						jComboBoxGroup = new JComboBox();
						jModelPanel.add(jComboBoxGroup, "4, 1");
						final JTextComponent editor = (JTextComponent) jComboBoxGroup.getEditor().getEditorComponent();
						editor.addFocusListener(new FocusAdapter() {
							@Override
							public void focusLost(final FocusEvent e) {
								m_bHasChanged = true;
								m_Algorithm.setGroup((String) jComboBoxGroup.getSelectedItem());
							}
						});
						final ComboBoxModel jComboBoxGroupModel = new DefaultComboBoxModel(getGroups());
						jComboBoxGroup.setModel(jComboBoxGroupModel);
						jComboBoxGroup.setEditable(true);
						jModelPanel.add(modelGraphPanel, "1, 2, 4, 2");
					}
					
					{
						/* this panel has buttons for file and node editing operations */
						jPanelButtonsModel = new JPanel();
						final TableLayout jPanelButtonsModelLayout =
							new TableLayout(new double[][] { { 	120.0, //col 0
																3.0,
																90.0,  //col 2
																3.0,
																90.0, // col 4																
																TableLayoutConstants.FILL,
																TableLayoutConstants.MINIMUM, // col 6
																TableLayoutConstants.MINIMUM, // col 7
																3.0,
																24.0, // col 9
																36.0, // col 10
																24.0, // col 11
																3.0
																},
								{ TableLayoutConstants.FILL } });
						jPanelButtonsModelLayout.setHGap(5);
						jPanelButtonsModelLayout.setVGap(5);
						jPanelButtonsModel.setLayout(jPanelButtonsModelLayout);
						jModelPanel.add(jPanelButtonsModel, "1, 4, 5, 4");						
						{
							/* popup menu for selecting New, Open, Save and Save As actions */
							jButtonMenu = new JButton();
							popup = new JPopupMenu();
					        popup.add(new JMenuItem(new AbstractAction(Sextante.getText("New")) {
					            public void actionPerformed(ActionEvent e) {
					            	checkChangesAndCreateNewModel();
					            }
					        }));
					        popup.add(new JMenuItem(new AbstractAction(Sextante.getText("Open")) {
					            public void actionPerformed(ActionEvent e) {
					            	checkChangesAndOpenModel();
					            }
					        }));
					        popup.add(new JSeparator(SwingConstants.HORIZONTAL));
					        
					        popup.add(jMenuSave);
				        	if ( m_Algorithm.getFilename() != null ) {
				        		jMenuSave.setEnabled(true);
				        	} else {
				        		jMenuSave.setEnabled(false);
				        	}
					        popup.add(new JMenuItem(new AbstractAction(Sextante.getText("Save_as")) {
					            public void actionPerformed(ActionEvent e) {
					            	saveModel(true);
					            }
					        }));					        
					        jButtonMenu.addMouseListener(new MouseAdapter() {
					            public void mousePressed(MouseEvent e) {
					                popup.show(e.getComponent(), e.getX(), e.getY());
					            }
					        });
							jButtonMenu.setText(Sextante.getText("file_operations"));
							jButtonMenu.setIcon(new ImageIcon(getClass().getClassLoader().
									getResource("javax/swing/plaf/metal/icons/ocean/menu.gif")));
							jButtonMenu.setIconTextGap(8);
							jPanelButtonsModel.add (jButtonMenu,"0, 0");					        
						}
						
						/* edit the selected node */
						jButtonEdit = new JButton();
						jButtonEdit.setText(Sextante.getText("Edit"));
						jButtonEdit.setEnabled(false);
						jButtonEdit.addActionListener(new ActionListener() {
							public void actionPerformed(final ActionEvent evt) {
								if ( currentNode != null )
									modelGraphPanel.editCell(currentNode);
							}
						});						
						jPanelButtonsModel.add (jButtonEdit,"2, 0");
						
						/* delete the selected node */
						jButtonDelete = new JButton();
						jButtonDelete.setText(Sextante.getText("Remove"));
						jButtonDelete.setEnabled(false);
						jButtonDelete.addActionListener(new ActionListener() {
							public void actionPerformed(final ActionEvent evt) {
								if ( currentNode != null ) {
									final String sKey = (String) (currentNode.getObject());
					            	removeElement(sKey);
								}
							}
						});							
						jPanelButtonsModel.add (jButtonDelete,"4, 0");
						
						
						/* controls for grid settings */
						
						jGridBox = new JCheckBox(Sextante.getText("modeler_grid_activate"));
						jGridBox.setSelected(false);
						jGridBox.setEnabled(true);
						jPanelButtonsModel.add (jGridBox,"6, 0");
						
						jGridSize = new JSpinner(new SpinnerNumberModel((int)dGridSize,1,100,1));
						jGridSize.setEnabled(false);
						jPanelButtonsModel.add (jGridSize,"7, 0");
												
						jGridSize.addChangeListener(new ChangeListener() {
							public void stateChanged(ChangeEvent e) {
								if ( jGridBox.isSelected() == true ) {
									final Integer value=(Integer) jGridSize.getValue();
									final int ival=value.intValue();
									modelGraphPanel.getGraph().setGridSize(ival);
								}
							}							
						});
						
						jGridBox.addActionListener(new ActionListener() {
							public void actionPerformed(final ActionEvent evt) {
								if ( jGridBox.isSelected() == true ) {
									modelGraphPanel.getGraph().setScale(dScale);
									modelGraphPanel.getGraph().setGridSize(dGridSize);
									modelGraphPanel.getGraph().setGridEnabled(true);
									modelGraphPanel.getGraph().setGridVisible(true);									
									jGridSize.setEnabled(true);
								} else {
									modelGraphPanel.getGraph().setScale(dScale);
									modelGraphPanel.getGraph().setGridEnabled(false);
									modelGraphPanel.getGraph().setGridVisible(false);
									jGridSize.setEnabled(false);
								}
							}
						});
					}
					
					jGridBox.addActionListener(new ActionListener() {
						public void actionPerformed(final ActionEvent evt) {
							if ( jGridBox.isSelected() == true ) {
								modelGraphPanel.getGraph().setGridSize(dGridSize);
								modelGraphPanel.getGraph().setGridEnabled(true);
								modelGraphPanel.getGraph().setGridVisible(true);
								jGridSize.setEnabled(true);
								modelGraphPanel.getGraph().setScale(2.0);
							} else {
								modelGraphPanel.getGraph().setGridEnabled(false);
								modelGraphPanel.getGraph().setGridVisible(false);
								jGridSize.setEnabled(false);
							}
						}
					});

					/* controls for scale settings */
					
					jScaleButtonMinus = new JButton(Sextante.getText("-"));
					jPanelButtonsModel.add (jScaleButtonMinus,"9, 0");

					jScaleButtonOne = new JButton(Sextante.getText("1:1"));
					jPanelButtonsModel.add (jScaleButtonOne,"10, 0");
					
					jScaleButtonPlus = new JButton(Sextante.getText("+"));
					jPanelButtonsModel.add (jScaleButtonPlus,"11, 0");
																
					jScaleButtonMinus.addActionListener(new ActionListener() {
						public void actionPerformed(final ActionEvent evt) {
							zoomMinus();
						}
					});
					
					jScaleButtonOne.addActionListener(new ActionListener() {
						public void actionPerformed(final ActionEvent evt) {
							zoomReset();
						}
					});					
					
					jScaleButtonPlus.addActionListener(new ActionListener() {
						public void actionPerformed(final ActionEvent evt) {
							zoomPlus();
						}
					});
					
					jElementsPanel = new JPanel();
					final TableLayout jElementsPanelLayout = 
							new TableLayout(new double[][] { { 3.0, TableLayoutConstants.FILL, 3.0 },
							{ 	3.0,
								TableLayoutConstants.FILL, // row 1: inputs selector
								40.0, // row 3: buttons panel ( Add | Help )
								3.0 } });
					jElementsPanelLayout.setHGap(5);
					jElementsPanelLayout.setVGap(5);
					jElementsPanel.setLayout(jElementsPanelLayout);
					jSplitPane.add(jElementsPanel, JSplitPane.LEFT);
					jSplitPane.setDividerLocation(0.3);
					jElementsPanel.setMinimumSize(new java.awt.Dimension(300, 528));
					{
						jPanelButtonsElements = new JPanel();
						final TableLayout jButtonsElementsPanelLayout = 
							new TableLayout(new double[][] { { 3.0, 
								120.0,
								TableLayoutConstants.FILL,
								40.0,
								3.0 },
							{ 	3.0,
								30.0,
								3.0 } });
						jButtonsElementsPanelLayout.setHGap(5);
						jButtonsElementsPanelLayout.setVGap(5);						
						jPanelButtonsElements.setLayout(jButtonsElementsPanelLayout);
						{
							jButtonAdd = new JButton();
							jButtonAdd.setText(Sextante.getText("Add") + "..." );
							jPanelButtonsElements.add(jButtonAdd,"1, 1");
							jButtonAdd.setEnabled(false); //only enable if a selection has been made from the tree
							jButtonAdd.addActionListener(new ActionListener() {
								public void actionPerformed(final ActionEvent evt) {
									switch (jElementsTabbedPane.getSelectedIndex()) {
									case 0:
										inputsPanel.addSelectedInput();
										break;
									case 1:
										extensionsPanel.addSelectedProcess();
										break;
									}
								}
							});
							jButtonHelp = new JButton();							
							//jButtonHelp.setText(Sextante.getText("Help"));
							jButtonHelp.setIcon(new ImageIcon(getClass().getClassLoader().getResource("images/info.gif")));
							jPanelButtonsElements.add(jButtonHelp, "3, 1");
							jButtonHelp.addActionListener(new ActionListener() {
								public void actionPerformed(final ActionEvent evt) {
									showHelp(evt);
								}
							});
						}
					}
					jElementsPanel.add(jPanelButtonsElements,"1, 2");
					{
						jElementsTabbedPane = new JTabbedPane();
						jElementsTabbedPane.setTabPlacement(SwingConstants.BOTTOM);
						jElementsPanel.add(jElementsTabbedPane, "1, 1");
						{
							inputsPanel = new InputsPanel(this, m_Parent);
							jElementsTabbedPane.addTab(Sextante.getText("Inputs"), null, inputsPanel, null);
							extensionsPanel = new AlgorithmsPanel(this, m_Parent);
							jElementsTabbedPane.addTab(Sextante.getText("Procedures"), null, extensionsPanel, null);
						}
						/* provide mouse and key listeners to toggle "Add.." button state */
						inputsPanel.getTree().addMouseListener(new MouseListener () {
							public void mouseClicked(MouseEvent e) {
								jButtonAdd.setEnabled(false);
								if ( inputsPanel.getTree().getSelectionPath() != null ) {
									final DefaultMutableTreeNode node = (DefaultMutableTreeNode) inputsPanel.getTree().
											getSelectionPath().getLastPathComponent();
							         if (node.getUserObject() instanceof ParameterPanel) {
							            final ParameterPanel paramPanel = (ParameterPanel) node.getUserObject();
							            if (paramPanel.parameterCanBeAdded()) {				
							            	jButtonAdd.setEnabled(true);
							            }
							         }									
								}
								jButtonAdd.repaint();
							}
							public void mouseEntered(MouseEvent e) {}
							public void mouseExited(MouseEvent e) {}
							public void mousePressed(MouseEvent e) {}
							public void mouseReleased(MouseEvent e) {}
						});
						inputsPanel.getTree().addKeyListener(new KeyListener () {
							public void keyReleased(KeyEvent e) {
								jButtonAdd.setEnabled(false);
								if ( inputsPanel.getTree().getSelectionPath() != null ) {
									final DefaultMutableTreeNode node = (DefaultMutableTreeNode) inputsPanel.getTree().
											getSelectionPath().getLastPathComponent();
							         if (node.getUserObject() instanceof ParameterPanel) {
							            final ParameterPanel paramPanel = (ParameterPanel) node.getUserObject();
							            if (paramPanel.parameterCanBeAdded()) {				
							            	jButtonAdd.setEnabled(true);
							            }
							         }									
								}
								jButtonAdd.repaint();								
							}
							public void keyTyped(KeyEvent e) {}							
							public void keyPressed(KeyEvent e) {}
							
						});
						/* provide mouse and key listeners to toggle "Add.." button state */
						extensionsPanel.getTree().addMouseListener(new MouseListener () {
							public void mouseClicked(MouseEvent e) {
								jButtonAdd.setEnabled(false);
								if ( extensionsPanel.getTree().getSelectionPath() != null ) {
							         final DefaultMutableTreeNode node = (DefaultMutableTreeNode) extensionsPanel.
							         		getTree().getSelectionPath().getLastPathComponent();
							         if ( node.getUserObject() instanceof java.lang.String == false ) {
							        	 final GeoAlgorithm alg = (GeoAlgorithm) node.getUserObject();
							        	 if (extensionsPanel.isAlgorithmEnabled(alg)) {
							        		 jButtonAdd.setEnabled(true);
							        	 }
							         }
								}
								jButtonAdd.repaint();
							}
							public void mouseEntered(MouseEvent e) {}
							public void mouseExited(MouseEvent e) {}
							public void mousePressed(MouseEvent e) {}
							public void mouseReleased(MouseEvent e) {}
						});
						extensionsPanel.getTree().addKeyListener(new KeyListener () {
							public void keyReleased(KeyEvent e) {
								jButtonAdd.setEnabled(false);
								if ( extensionsPanel.getTree().getSelectionPath() != null ) {
									final DefaultMutableTreeNode node = (DefaultMutableTreeNode) extensionsPanel.getTree().
											getSelectionPath().getLastPathComponent();
							         if (node.getUserObject() instanceof ParameterPanel) {
							            final ParameterPanel paramPanel = (ParameterPanel) node.getUserObject();
							            if (paramPanel.parameterCanBeAdded()) {				
							            	jButtonAdd.setEnabled(true);
							            }
							         }									
								}
								jButtonAdd.repaint();								
							}
							public void keyTyped(KeyEvent e) {}							
							public void keyPressed(KeyEvent e) {}
							
						});						
					}					
				}
			}
		}

	}

	
	public void toggleEditButtons ( boolean active, ObjectAndDescription node ) {
		if ( jButtonEdit != null && jButtonDelete != null ) {
			if ( active == true ) {
				jButtonEdit.setEnabled(true);
				jButtonDelete.setEnabled(true);
				currentNode = node;
			} else {
				jButtonEdit.setEnabled(false);
				jButtonDelete.setEnabled(false);
				currentNode = null;
			}
			jButtonEdit.repaint();
			jButtonDelete.repaint();			
		}
	}

	
	public void zoomMinus () {
		if ( dScale > 0.2 ) {
			dScale = dScale * 0.90;
			modelGraphPanel.getGraph().setScale(dScale);
		}
	}

	
	public void zoomPlus () {
		if ( dScale < 2.0 ) {
			dScale = dScale * 1.10;
			modelGraphPanel.getGraph().setScale(dScale);
		}
	}	
	
	
	public void zoomReset () {
		dScale = 1.0;
		modelGraphPanel.getGraph().setScale(dScale);
	}	
	
	
	private String[] getGroups() {

		final ArrayList<String> groups = new ArrayList<String>();

		groups.add(Sextante.getText("Models"));
		final HashMap<String, GeoAlgorithm> algs = Sextante.getAlgorithms().get("SEXTANTE");
		final Set<String> keys = algs.keySet();
		final Iterator<String> iter = keys.iterator();
		while (iter.hasNext()) {
			final GeoAlgorithm alg = algs.get(iter.next());
			if (!groups.contains(alg.getGroup())) {
				groups.add(alg.getGroup());
			}
		}


		final String[] sortedGroups = groups.toArray(new String[0]);
		Arrays.sort(sortedGroups);

		return sortedGroups;

	}


	protected void showHelp(final ActionEvent evt) {

		SextanteGUI.getGUIFactory().showHelpDialog("modeler");

	}


	public ModelGraphPanel getGraph() {

		return modelGraphPanel;

	}


	public void checkChangesAndOpenModel(final String sFilename) {

		if (m_bHasChanged) {
			final int iRet = JOptionPane.showConfirmDialog(null,
					Sextante.getText("Model_has_been_modified") + "\n"
					+ Sextante.getText("Do_you_want_to_open_a_new_model_without_saving_changes"),
					Sextante.getText("Warning"), JOptionPane.YES_NO_CANCEL_OPTION);
			if (iRet == JOptionPane.YES_OPTION) {
				openModel(sFilename);
			}
		}
		else {
			openModel(sFilename);
		}

	}
	
	
	public void checkChangesAndCloseModel() {

		if (m_bHasChanged) {
			final int iRet = JOptionPane.showConfirmDialog(null,
					Sextante.getText("Model_has_been_modified") + "\n"
					+ Sextante.getText("Do_you_want_to_save_your_changes"),
					Sextante.getText("Warning"), JOptionPane.YES_NO_OPTION);
			if (iRet == JOptionPane.YES_OPTION) {
				saveModel(false);
			}
		}
	}


	private void openModel(final String sFilename) {

		newModel();

		if (sFilename != null) {
			final File file = new File(sFilename);
			try {
				m_Algorithm = ModelAlgorithmIO.open(file, this);
				extensionsPanel.setAlgorithm(m_Algorithm);
				extensionsPanel.setAlgorithmCount(m_Algorithm.getAlgorithms().size() + 1);
				updatePanel(false);
				jTextFieldName.setText(m_Algorithm.getName());
				final JTextField textField = (JTextField) jComboBoxGroup.getEditor().getEditorComponent();
				textField.setText(m_Algorithm.getGroup());
			}
			catch (final Exception e) {
				Sextante.addErrorToLog(e);
				return;
			}
			jMenuSave.setEnabled(true);
		}

		m_bHasChanged = false;

	}


	protected void checkChangesAndOpenModel() {

		if (m_bHasChanged) {
			final int iRet = JOptionPane.showConfirmDialog(null,
					Sextante.getText("Model_has_been_modified") + "\n"
					+ Sextante.getText("Do_you_want_to_open_a_new_model_without_saving_changes"),
					Sextante.getText("Warning"), JOptionPane.YES_NO_CANCEL_OPTION);
			if (iRet == JOptionPane.YES_OPTION) {
				openModel();
			}
		}
		else {
			openModel();
		}

	}


	protected void saveModel( boolean SaveAs) {

		String sFilename = m_Algorithm.getFilename();
		final JFileChooser fc = new JFileChooser();
		final GenericFileFilter javaFilter = new GenericFileFilter("java", "Java code (*.java)");
		final ModelFileFilter modelFilter = new ModelFileFilter();
		fc.addChoosableFileFilter(modelFilter);
		fc.addChoosableFileFilter(javaFilter);
		fc.setAcceptAllFileFilterUsed(false);
		fc.setFileFilter(modelFilter);
		if (sFilename != null) {
			fc.setSelectedFile(new File(sFilename));
		}
		else {
			final String sFolder = SextanteGUI.getSettingParameterValue(SextanteModelerSettings.MODELS_FOLDER);
			fc.setCurrentDirectory(new File(sFolder));
		}
		
		/* we only show a "Save As..." dialog if it is really necessary */
		int returnVal;
		if ( SaveAs == true || m_Algorithm.getFilename() == null ) {
			returnVal = fc.showSaveDialog(this);
		} else {
			returnVal = JFileChooser.APPROVE_OPTION;
		}		

		File file = null;
		if (returnVal == JFileChooser.APPROVE_OPTION) {
			if ( SaveAs == true || m_Algorithm.getFilename() == null ) {
				file = fc.getSelectedFile();
				sFilename = file.getAbsolutePath();
				m_Algorithm.setFilename(sFilename);
			} else {
				sFilename = m_Algorithm.getFilename();
				file = new File(sFilename);
			}
			if (fc.getFileFilter() == javaFilter) {
				/* this can only happen if we have a "Save As..." action */
				if (!sFilename.endsWith("java")) {
					file = new File(sFilename + ".java");
				}
				ModelAlgorithmIO.saveAsJava(m_Algorithm, file);
			}
			else {
				if (!sFilename.endsWith("model")) {
					file = new File(sFilename + ".model");
					jMenuSave.setEnabled(true);
				}
				modelGraphPanel.storeCoords();
				ModelAlgorithmIO.save(this, file);
				m_bHasChanged = false;
				SextanteGUI.updateAlgorithmProvider(ModelerAlgorithmProvider.class);
				SextanteGUI.getGUIFactory().updateToolbox();
			}
		}

	}


	protected void openModel() {		
		
		final JFileChooser fc = new JFileChooser();
		final ModelFileFilter filter = new ModelFileFilter();

		final String sFolder = SextanteGUI.getSettingParameterValue(SextanteModelerSettings.MODELS_FOLDER);
		fc.setFileFilter(filter);
		fc.setCurrentDirectory(new File(sFolder));
		final int returnVal = fc.showOpenDialog(this);

		if (returnVal == JFileChooser.APPROVE_OPTION) {
			final File file = fc.getSelectedFile();
			try {
				newModel();
				m_Algorithm = ModelAlgorithmIO.open(file, this);
				extensionsPanel.setAlgorithm(m_Algorithm);
				extensionsPanel.setAlgorithmCount(m_Algorithm.getAlgorithms().size() + 1);
				updatePanel(false);
				jTextFieldName.setText(m_Algorithm.getName());
				updatePanel(false);
			}
			catch (final Exception e) {
				Sextante.addErrorToLog(e);
				return;
			}
		}
		jMenuSave.setEnabled(true);
		m_bHasChanged = false;
	}


	protected void checkChangesAndCreateNewModel() {

		if (m_bHasChanged) {
			final int iRet = JOptionPane.showConfirmDialog(null,
					Sextante.getText("Model_has_been_modified") + "\n"
					+ Sextante.getText("Do_you_want_to_start_a_new_model_without_saving_changes?"),
					Sextante.getText("Warning"), JOptionPane.YES_NO_CANCEL_OPTION);
			if (iRet == JOptionPane.YES_OPTION) {
				newModel();
			}
		}
		else {
			newModel();
		}


	}


	public void updatePanel(final boolean bUpdateCoords) {

		updateGraphicalDescription(bUpdateCoords);
		//updateButtons();

	}


	/*   private void updateButtons() {

         final Object[] objs = SextanteGUI.getInputFactory().getDataObjects();
         jButtonExecute.setEnabled(m_Algorithm.meetsDataRequirements(objs));

      }*/


	private void updateGraphicalDescription(final boolean bUpdateCoords) {

		if (bUpdateCoords) {
			modelGraphPanel.storeCoords();
		}
		modelGraphPanel.updateGraph();

	}


	private void newModel() {

		m_bHasChanged = false;
		m_Algorithm = new ModelAlgorithm();
		m_Algorithm.setGroup(Sextante.getText("Models"));
		m_DataObjects.clear();
		m_InputKeys.clear();
		extensionsPanel.setAlgorithm(m_Algorithm);
		extensionsPanel.setAlgorithmCount(0);
		modelGraphPanel.setAlgorithm(m_Algorithm);
		modelGraphPanel.resetCoords();
		jTextFieldName.setText(Sextante.getText("[New_model]"));
		jComboBoxGroup.setSelectedItem(Sextante.getText("Models"));
		jMenuSave.setEnabled(false);
		dScale = 1.0;
		modelGraphPanel.getGraph().setScale(dScale);
		updatePanel(true);
	}


	private void removeAlgorithm(final String sAlgKey) {

		OutputObjectsSet ooSet;
		Set set;
		Iterator iter;
		final GeoAlgorithm alg = m_Algorithm.getAlgorithm(sAlgKey);
		String sKey;
		final ArrayList toRemove = new ArrayList();

		ooSet = alg.getOutputObjects();
		for (int i = 0; i < ooSet.getOutputObjectsCount(); i++) {
			final Output out = ooSet.getOutput(i);
			sKey = out.getName();
			sKey += sAlgKey;
			m_Algorithm.unassign(sKey);
			m_Algorithm.getOutputObjects().remove(sKey);
			m_DataObjects.remove(sKey);
		}

		set = m_DataObjects.keySet();
		iter = set.iterator();
		while (iter.hasNext()) {
			final Object obj = iter.next();
			if (obj instanceof String) {
				sKey = (String) obj;
				if (sKey.startsWith("INNERPARAM") && sKey.endsWith(sAlgKey)) {
					toRemove.add(sKey);
				}
			}
		}

		for (int i = 0; i < toRemove.size(); i++) {
			m_DataObjects.remove(toRemove.get(i));
		}

		m_Algorithm.removeAlgorithm(sAlgKey);
		m_bHasChanged = true;

	}


	private void removeDataObject(final String sKey) {

		m_Algorithm.removeInput(sKey);
		m_DataObjects.remove(sKey);
		m_InputKeys.remove(sKey);
		//modelGraphPanel.removeCell(sKey);
		m_bHasChanged = true;

	}


	public void removeElement(final String sKey) {

		final Object obj = getObjectFromKey(sKey);

		if (obj instanceof GeoAlgorithm) {
			if (canRemoveAlgorithm(sKey)) {
				final int iRet = JOptionPane.showConfirmDialog(null,
						Sextante.getText("delete_modeler_node_question"),
						Sextante.getText("Warning"), JOptionPane.YES_NO_CANCEL_OPTION);				
				if (iRet == JOptionPane.YES_OPTION) {
					removeAlgorithm(sKey);
				}
				updatePanel(true);
			}
			else {
				JOptionPane.showMessageDialog(null, Sextante.getText("Other_elements_depend_on_the_selected_one") + ".\n"
						+ Sextante.getText("Remove_them_before_removing_this_one"),
						Sextante.getText("Warning"), JOptionPane.WARNING_MESSAGE);
			}
		}
		else {
			if (canRemoveDataObject(sKey)) {
				removeDataObject(sKey);
				updatePanel(true);
			}
			else {
				JOptionPane.showMessageDialog(null, Sextante.getText("Other_elements_depend_on_the_selected_one") + ".\n"
						+ Sextante.getText("Remove_them_before_removing_this_one"),
						Sextante.getText("Warning"), JOptionPane.WARNING_MESSAGE);
			}
		}

	}


	private boolean canRemoveAlgorithm(final String sKey) {

		String sObjectKey;
		final GeoAlgorithm alg = m_Algorithm.getAlgorithm(sKey);
		OutputObjectsSet ooSet = alg.getOutputObjects();
		ooSet = alg.getOutputObjects();
		for (int i = 0; i < ooSet.getOutputObjectsCount(); i++) {
			final Output out = ooSet.getOutput(i);
			sObjectKey = out.getName() + sKey;
			if (!canRemoveDataObject(sObjectKey)) {
				return false;
			}
		}

		return true;
	}


	private boolean canRemoveDataObject(final String sKey) {

		int i;
		final ArrayList algorithmKeys = m_Algorithm.getAlgorithmKeys();
		String sAlgKey;

		for (i = 0; i < algorithmKeys.size(); i++) {
			sAlgKey = (String) algorithmKeys.get(i);
			final HashMap assignments = m_Algorithm.getInputAssignments(sAlgKey);
			final Set set = assignments.keySet();
			final Iterator iter = set.iterator();
			String sAssignmentKey;
			String sAssignment;
			while (iter.hasNext()) {
				sAssignmentKey = (String) iter.next();
				sAssignment = (String) assignments.get(sAssignmentKey);
				if (sAssignment != null) {
					if (sAssignment.equals(sKey)) {
						return false;
					}
					else if (sAssignment.startsWith("INNERPARAM")) {
						//if it is a multiple input, check against its individual data objects
						final Object obj = ((ObjectAndDescription) getDataObjects().get(sAssignment)).getObject();
						if (obj instanceof ArrayList) {
							final ArrayList list = (ArrayList) obj;
							for (int j = 0; j < list.size(); j++) {
								final String s = (String) list.get(j);
								if (s.equals(sKey)) {
									return false;
								}
							}
						}
					}
				}
			}
		}

		return true;

	}


	/*private void executeModel() {

      m_Algorithm.getInputs().clear();

      final Set set = m_DataObjects.keySet();
      final Iterator iter = set.iterator();
      while (iter.hasNext()) {
         final String sKey = (String) iter.next();
         final ObjectAndDescription oad = (ObjectAndDescription) m_DataObjects.get(sKey);
         m_Algorithm.getInputs().put(sKey, oad.getObject());
      }

      try {
         final GeoAlgorithm alg = m_Algorithm.getNewInstance();
         final int iRet = SextanteGUI.getGUIFactory().showAlgorithmDialog(alg, m_Parent, null);
         if (iRet == IGUIFactory.OK) {
            GeoAlgorithmExecutors.execute(alg, m_Parent);
         }
      }
      catch (final Exception e) {
         Sextante.addErrorToLog(e);
      }

   }*/


	public boolean hasChanged() {

		return m_bHasChanged;

	}


	public void setHasChanged(final boolean hasChanged) {

		m_bHasChanged = hasChanged;

	}


	public Object getObjectFromKey(final String sObjectKey) {

		int i;
		String sKey;

		for (i = 0; i < m_InputKeys.size(); i++) {
			sKey = (String) m_InputKeys.get(i);
			if (sKey.equals(sObjectKey)) {
				return m_DataObjects.get(sKey);
			}
		}

		final ArrayList algKeys = m_Algorithm.getAlgorithmKeys();

		for (i = 0; i < algKeys.size(); i++) {
			sKey = (String) algKeys.get(i);
			if (sKey.equals(sObjectKey)) {
				return m_Algorithm.getAlgorithm(sKey);
			}
		}

		return null;

	}


	public void addInputToArray(String sKey,
			final Object obj,
			final ArrayList array) {

		int i;
		Object input;
		if (obj instanceof ArrayList) {
			final ArrayList multipleInput = (ArrayList) obj;
			for (i = 0; i < multipleInput.size(); i++) {
				sKey = (String) multipleInput.get(i);
				input = ((ObjectAndDescription) m_DataObjects.get(sKey)).getObject();
				if (input != null) {
					addInputToArray(sKey, multipleInput.get(i), array);
				}
			}
		}
		else {
			array.add(sKey);
		}

		m_bHasChanged = true;

	}


	private ArrayList getArrayOfSingleInputs(final HashMap assignments) {

		Set set;
		Iterator iter;
		String sKey;
		String sInput;
		Object obj;
		final ArrayList array = new ArrayList();

		set = assignments.keySet();
		iter = set.iterator();
		while (iter.hasNext()) {
			sKey = (String) iter.next();
			sInput = (String) assignments.get(sKey);
			if (sInput != null) {
				obj = ((ObjectAndDescription) m_DataObjects.get(sInput)).getObject();
				addInputToArray(sInput, obj, array);
			}
		}

		return array;

	}


	public ArrayList getDependences(final String sKey) {

		int i, j;
		boolean bFoundMatch;
		final ArrayList dependences = new ArrayList();
		GeoAlgorithm alg = m_Algorithm.getAlgorithm(sKey);
		final HashMap assignments = m_Algorithm.getInputAssignments(sKey);
		final ArrayList algorithms = m_Algorithm.getAlgorithms();
		final ArrayList algorithmKeys = m_Algorithm.getAlgorithmKeys();
		OutputObjectsSet ooSet;
		String sInput, sInputKey, sOutput;
		String sAlgKey;

		if (alg == null) {
			return null;
		}

		final ArrayList inputs = getArrayOfSingleInputs(assignments);
		for (j = 0; j < inputs.size(); j++) {
			sInput = (String) inputs.get(j);
			bFoundMatch = false;
			for (i = 0; (i < algorithms.size()) && !bFoundMatch; i++) {
				alg = (GeoAlgorithm) algorithms.get(i);
				sAlgKey = (String) algorithmKeys.get(i);
				ooSet = alg.getOutputObjects();
				for (int k = 0; k < ooSet.getOutputObjectsCount(); k++) {
					final Output out = ooSet.getOutput(k);
					sOutput = out.getName();
					sOutput += sAlgKey;
					if (sInput.equals(sOutput)) {
						bFoundMatch = true;
						if (!dependences.contains(sAlgKey)) {
							dependences.add(sAlgKey);
						}
						break;
					}
				}
			}
			if (!bFoundMatch) {
				for (i = 0; (i < m_InputKeys.size()) && !bFoundMatch; i++) {
					sInputKey = (String) m_InputKeys.get(i);
					if (sInput.equals(sInputKey)) {
						bFoundMatch = true;
						if (!dependences.contains(sInputKey)) {
							dependences.add(sInputKey);
						}
						break;
					}
				}
			}
		}

		return dependences;

	}


	public ModelAlgorithm getAlgorithm() {

		return m_Algorithm;

	}


	public HashMap getDataObjects() {

		return m_DataObjects;

	}


	public ArrayList getInputKeys() {

		return m_InputKeys;

	}


	public ModelGraphPanel getModelGraphPanel() {

		return modelGraphPanel;

	}

}

