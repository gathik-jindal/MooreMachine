/**
 * This is the Block class that stores the information that all blocks needs to have. 
 * 
 * @author Aryan, Abhirath, Gathik
 * @version 1.0
 * @since 06/08/2024
 */

import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Polygon;
import java.awt.Rectangle;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import java.awt.geom.Line2D;

import java.io.File;

import java.text.NumberFormat;

import java.util.LinkedHashMap;
import java.util.Map;

import javax.swing.BorderFactory;
import javax.swing.InputVerifier;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JFileChooser;
import javax.swing.JFormattedTextField;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JSpinner;
import javax.swing.JTextField;
import javax.swing.SpinnerNumberModel;

import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

import javax.swing.text.DefaultFormatterFactory;
import javax.swing.text.NumberFormatter;

/**
 * The Block class stores the information that is inherent to all blockss
 */
public abstract class Block 
{
    private Rectangle rect;                 //rectangle object for rectangular blocks
    private Line2D.Double line;             //line object for wires
    private Color color;                    //color of the block
    private String name;                    //name of the block
    private Map<String, Component> map;     //map that stores all the fields
    private DrawCircuit drawingPanel;      //drawingPanel in which the block would be drawn
    private int currID = 0;                 //the id of this block
    private static int id = 0;              //to assign new id to each new block

    /**
     * Creates a new block object
     * @param name : the name of the block
     * @param rect : the rectangle that is drawn
     * @param color : the color of the rectangle
     * @param panel : the DrawCircuit in which the rectangle is drawn
     */
    public Block(String name, Rectangle rect, Color color, DrawCircuit panel) 
    {
        this.name = name;
        this.rect = rect;
        this.color = color;
        this.map = new LinkedHashMap<>();
        this.drawingPanel = panel;
        this.currID = id;

        id++;
    }

    public static void reset()
    {
        id = 0;
    }

    /**
     * Creates a new block object
     * @param name : the name of the block
     * @param line : the line that is drawn
     * @param color : the color of the line
     * @param panel : the DrawCircuit in which the line is drawn
     */
    public Block(String name, Line2D.Double line, Color color, DrawCircuit panel)
    {
        this.name = name;
        this.line = line;
        this.color = color;
        this.map = new LinkedHashMap<>();
        this.drawingPanel = panel;
        this.currID = id;

        id++;
    }

    /**
     * Sets the rectangle object with the given color
     * @param rect : the new rectangle object
     * @param color : the color of the rectangle
     */
    public void setRect(Rectangle rect, Color color) 
    {
        this.rect = rect;
        this.color = color;
    }

    /**
     * Sets the line object with the given color
     * @param line : the new line object
     * @param color : the color of the line
     */
    public void setLine(Line2D.Double line, Color color)
    {
        this.line = line;
        this.color = color;
    }

    /**
     * @return the rectangle that is drawn
     */
    public Rectangle getRect() 
    {
        return this.rect;
    }

    /**
     * @return the line that is drawn
     */
    public Line2D.Double getLine()
    {
        return this.line;
    }

    /**
     * @return the color of the line or the rectangle
     */
    public Color getColor() 
    {
        return this.color;
    }

    /**
     * @return name the of the block
     */
    public String getName() 
    {
        if(map.containsKey("blockID"))
            return ((JTextField)(map.get("blockID"))).getText();
        
        return this.name;
    }

    /**
     * @return the map that stores all the fields of the block
     */
    public Map<String, Component> getMap()
    {
        return this.map;
    }

    /**
     * Sets the field map to the map given
     * @param fields the new map containing the fields
     */
    public void setMap(Map<String, Component> fields)
    {
        this.map = fields;
    }

    /**
     * Applies formatting to the component given
     * @param component : the component to apply formatting to
     */
    private void applyFormatting(Component component)
    {
        component.setFont(new Font("Arial", Font.PLAIN, 9));
        component.setPreferredSize(new Dimension(200, 20));
        component.setMaximumSize(new Dimension(200, 20));
        component.setBackground(Color.WHITE);
    }

    /**
     * @param value : the starting value in the JTextField
     * @return JTextField object with the starting value specified
     */
    protected JTextField createTextField(String value)
    {
        JTextField jTextField = new JTextField(value);
        
        applyFormatting(jTextField);
        jTextField.setEditable(true);
        jTextField.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        
        //repaint whenever the field is updated
        jTextField.getDocument().addDocumentListener(new DocumentListener() 
        {
            @Override
            public void insertUpdate(DocumentEvent e) 
            {
                drawingPanel.repaint();
            }

            @Override
            public void removeUpdate(DocumentEvent e) 
            {
                drawingPanel.repaint();            
            }

            @Override
            public void changedUpdate(DocumentEvent e) 
            {
                drawingPanel.repaint();            
            }

        });

        return jTextField;
    }

    /**
     * Creats a new button that can access files
     * @param value : the text on the button
     * @param field : the JTextField whose text field would be set to the new path
     * @return JButton that can access files
     */
    protected JButton createFileButton(String value, JTextField field)
    {
        JButton button = new JButton(value);
        applyFormatting(button);
        button.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        button.setBackground(new Color(173, 216, 230));

        button.addActionListener(new ActionListener() 
        {
            @Override
            public void actionPerformed(ActionEvent e) 
            {
                JFileChooser fileChooser = new JFileChooser();
        
                fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
        
                int result = fileChooser.showOpenDialog(null);
        
                if (result == JFileChooser.APPROVE_OPTION) 
                {
                    File selectedFile = fileChooser.getSelectedFile();
        
                    field.setText(selectedFile.getAbsolutePath());
                }
            }
        });

        button.addMouseListener(new MouseAdapter() 
        {
            @Override
            public void mouseEntered(MouseEvent evt) 
            {
                button.setBackground(Color.CYAN);
            }

            @Override
            public void mouseExited(MouseEvent evt) 
            {
                button.setBackground(new Color(173, 216, 230));
            }
        });

        return button;
    }

    /**
     * Creates a new Spinner object with the initial value, the minimum value, and the maximum value
     * @param value : the initial value
     * @param min : the minimum value
     * @param max : the maximum value
     * @return JSpinner object with the above specifications
     */
    protected JSpinner createIntField(int value, int min, int max)
    {
        SpinnerNumberModel numberModel = new SpinnerNumberModel(value, min, max, 1);
        JSpinner spinner = new JSpinner(numberModel);

        applyFormatting(spinner);
        spinner.setBorder(BorderFactory.createLineBorder(Color.GRAY));

        JComponent editor = spinner.getEditor();
        JFormattedTextField textField = ((JSpinner.DefaultEditor) editor).getTextField();
        textField.setHorizontalAlignment(JTextField.LEFT);

        NumberFormat format = NumberFormat.getIntegerInstance();
        NumberFormatter numberFormatter = new NumberFormatter(format);
        numberFormatter.setValueClass(Integer.class);
        numberFormatter.setMinimum(min);
        numberFormatter.setMaximum(max);
        numberFormatter.setAllowsInvalid(false);
        numberFormatter.setCommitsOnValidEdit(true);

        textField.setFormatterFactory(new DefaultFormatterFactory(numberFormatter));

        return spinner;
    }

    /**
     * Creates a JTextField that only accpets floating point numbers
     * @param initialValue : the initial value of the JTextField
     * @return JTextField with the above specifications
     */
    protected JTextField createFloatField(double initialValue) 
    {
        JTextField numberField = new JTextField(initialValue + "");
        
        applyFormatting(numberField);
        numberField.setEditable(true);
        numberField.setBorder(BorderFactory.createLineBorder(Color.GRAY));

        numberField.setInputVerifier(new InputVerifier() 
        {
            @Override
            public boolean verify(JComponent input) 
            {
                JTextField textField = (JTextField) input;
                String text = textField.getText();
                
                try 
                {
                    Double.parseDouble(text);
                    return true;
                } 
                catch (NumberFormatException e) 
                {
                    numberField.setText(initialValue + "");
                    return false;
                }
            }
        });

        return numberField;
    }

    /**
     * Creates a JComboBox with the given options and the given starting selected option
     * @param options : the options of the ComboBox
     * @param selectedOption : the starting selected options
     * @return JComboBox<String> with the above specifications
     */
    protected JComboBox<String> createOptions(String [] options, String selectedOption)
    {
        JComboBox<String> comboBox = new JComboBox<>(options);
        comboBox.setSelectedItem(selectedOption);

        applyFormatting(comboBox);
        comboBox.setEditable(false);
        comboBox.setBorder(BorderFactory.createLineBorder(Color.GRAY));

        comboBox.addActionListener(new ActionListener() 
        {
            @Override
            public void actionPerformed(ActionEvent e) 
            {
                drawingPanel.repaint();
            }
            
        });

        return comboBox;
    }

    /**
     * Creates a new label
     * @return JLabel with the above specifications
     */
    protected JLabel createLabel()
    {
        JLabel label = new JLabel();
        applyFormatting(label);
        label.setBorder(BorderFactory.createLineBorder(Color.GRAY));

        return label;
    }

    /**
     * Creates a new JButton that deletes this block if pressed after confirmation
     * @param str : the text on the JButton
     * @return JButton with the above specifications
     */
    protected JButton createDeleteButton(String str)
    {
        JButton button = new JButton(str);
        applyFormatting(button);
        button.setBackground(new Color(178, 34, 34));
        button.setForeground(Color.WHITE);

        button.addMouseListener(new MouseAdapter() 
        {
            @Override
            public void mouseEntered(MouseEvent evt) 
            {
                button.setBackground(Color.RED);
            }

            @Override
            public void mouseExited(MouseEvent evt) 
            {
                button.setBackground(new Color(178, 34, 34));
            }
        });

        Block b = this;
        button.addActionListener(new ActionListener() 
        {
            @Override
            public void actionPerformed(ActionEvent e) 
            {
                int option = JOptionPane.showInternalConfirmDialog(null, "Are you sure you want to delete this block?", 
                            "Delete Block?", JOptionPane.YES_NO_OPTION, JOptionPane.WARNING_MESSAGE);
                
                if(option == 0)
                    drawingPanel.deleteBlock(b);
            }
        });

        return button;
    }

    /**
     * @return String representation of the block 
     */
    @Override
    public String toString()
    {
        return currID + "";
    }

    /**
     * @return "True" if plot is set to true; "False" otherwise
     */
    @SuppressWarnings("unchecked")
    public String getPlot()
    {
        return (String)(((JComboBox<String>)(map.get("plot"))).getSelectedItem());
    }

    /**
     * @return the block id of the block
     */
    public String getBlockID()
    {
        return (String)(((JTextField)(map.get("blockID"))).getText());
    }
}

/**
 * All blocks except for wires are rectangular boxes
 */
abstract class RectangleBlock extends Block
{
    /**
     * Creates a new RectangleBox
     * @param name : the name of the block
     * @param rect : the rectangle that is to be drawn
     * @param color : the color of the block
     * @param panel : the DrawCircuit on which the rectangle is to be drawn
     */
    public RectangleBlock(String name, Rectangle rect, Color color, DrawCircuit panel)
    {
        super(name, rect, color, panel);
    }

    /**
     * @return true if the block has output connections; false otherwise
     */
    public abstract boolean hasOutput();

    /**
     * @return true if the block has input connections; false otherwise
     */
    public abstract boolean hasInput();

    /**
     * @return String representation of the type of object
     */
    public abstract String getType();

    /**
     * @return String representation of the object name which will be written in the python file
     */
    public abstract String getObjectName();
}

class Moore extends RectangleBlock
{
    /**
     * Creates a Moore machine block.
     * @param name : the name of the block
     * @param rect : the rectangle which is to be drawn
     * @param color : the color of the rectangle
     * @param panel : the DrawCircuit on which the rectangle is to be drawn
     */
    public Moore(String name, Rectangle rect, Color color, DrawCircuit panel)
    {
        super(name, rect, color, panel);
        LinkedHashMap<String, Component> map = new LinkedHashMap<>();
        map.put("maxOutSize", createIntField(1, 0, Integer.MAX_VALUE));
        map.put("plot", createOptions(new String [] {"True", "False"}, "False"));
        map.put("blockID", createTextField(name));
        map.put("nsl", createTextField("lambda ps, i: 0"));
        map.put("ol", createTextField("lambda ps, i: 0"));
        map.put("startingState", createIntField(0, 0, Integer.MAX_VALUE));
        map.put("risingEdge", createOptions(new String [] {"True", "False"}, "True"));
        map.put("nsl_delay", createTextField("0.01"));
        map.put("ol_delay", createTextField("0.01"));
        map.put("register_delay", createTextField("0.01"));

        map.put("Delete", createDeleteButton("Delete Moore Machine"));
        setMap(map);
    }

    /**
     * @return String representation of the Block
     */
    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.moore(maxOutSize = "+getMaxOutSize() + ", plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\"" +  
            ", nsl = " + getNSL() +", ol = " + getOL() + ", startingState = " + getStartingState() + ", risingEdge = " + getRisingEdge() +
            ", nsl_delay = " + getNSLDelay() + ", ol_delay = " + getOLDelay() + ", register_delay = " + getRegisterDelay()  + ")";
    }

    /**
     * @return the maximum output wires of the Moore Machine
     */
    public Integer getMaxOutSize()
    {
        return (Integer)(((JSpinner)(getMap().get("maxOutSize"))).getValue());
    }

    /**
     * @return the next state logic of the machine
     */
    public String getNSL()
    {
        return (String)(((JTextField)(getMap().get("nsl"))).getText());
    }

    /**
     * @return the output logic of the machine
     */
    public String getOL()
    {
        return (String)(((JTextField)(getMap().get("ol"))).getText());
    }

    /**
     * @return the starting state of the machine
     */
    public Integer getStartingState()
    {
        return (Integer)(((JSpinner)(getMap().get("startingState"))).getValue());
    }

    /**
     * @return true if the registers should change on the rising edge of the clock; false otherwise
     */
    @SuppressWarnings("unchecked")
    public String getRisingEdge()
    {
        return (String)(((JComboBox<String>)(getMap().get("risingEdge"))).getSelectedItem());
    }

    /**
     * @return the next state logic delay of the machine
     */
    public String getNSLDelay()
    {
        return (String)(((JTextField)(getMap().get("nsl_delay"))).getText());
    }

    /**
     * @return the output logic delay of the machine
     */
    public String getOLDelay()
    {
        return (String)(((JTextField)(getMap().get("ol_delay"))).getText());
    }

    /**
     * @return the register delay of the machine
     */
    public String getRegisterDelay()
    {
        return (String)(((JTextField)(getMap().get("register_delay"))).getText());
    }

    /**
     * @return String representation of the object name which will be written in the python file
     */
    @Override
    public String getObjectName()
    {
        return "moore" + super.toString();
    }

    /**
     * @return true
     */
    @Override
    public boolean hasOutput() 
    {
        return true;
    }
    
    /**
     * @return true
     */
    @Override
    public boolean hasInput() 
    {
        return true;
    }

    /**
     * @return the type of the block ("Moore")
     */
    @Override
    public String getType() 
    {
        return "Moore";
    }
}

class Mealy extends Moore
{
     /**
     * Creates a Mealy machine block.
     * @param name : the name of the block
     * @param rect : the rectangle which is to be drawn
     * @param color : the color of the rectangle
     * @param panel : the DrawCircuit on which the rectangle is to be drawn
     */
    public Mealy(String name, Rectangle rect, Color color, DrawCircuit panel)
    {
        super(name, rect, color, panel);
    }

    /**
     * @return String representation of the Block
     */
    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.mealy(maxOutSize = "+getMaxOutSize() + ", plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\"" +  
            ", nsl = " + getNSL() +", ol = " + getOL() + ", startingState = " + getStartingState() + ", risingEdge = " + getRisingEdge() +
            ", nsl_delay = " + getNSLDelay() + ", ol_delay = " + getOLDelay() + ", register_delay = " + getRegisterDelay()  + ")";
    }

    /**
     * @return String representation of the object name which will be written in the python file
     */
    @Override
    public String getObjectName()
    {
        String parent = super.getObjectName();
        return "mealy" + parent.substring(parent.indexOf("moore") + 5);
    }

    /**
     * @return the type of the block ("Mealy")
     */
    public String getType()
    {
        return "Mealy";
    }
}

class Input extends RectangleBlock
{
    /**
     * Creates a new Input block
     * @param name : the name of the block
     * @param rect : the Rectangle object which is to be drawn
     * @param color : the color of the Rectangle
     * @param panel : the DrawCircuitignPanel on which the rectangle would be drawn
     */
    public Input(String name, Rectangle rect, Color color, DrawCircuit panel)
    {
        super(name, rect, color, panel);
        LinkedHashMap<String, Component> map = new LinkedHashMap<>();
        map.put("filePath", createTextField("filePath"));
        map.put("", createFileButton("Choose File", (JTextField)(map.get("filePath"))));
        map.put("plot", createOptions(new String [] {"True", "False"}, "False"));
        map.put("blockID", createTextField(name));
        map.put("Delete", createDeleteButton("Delete Input Block"));
        setMap(map);
    }

    /**
     * @return String representation of the block
     */
    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.source(filePath = \""+getFilePath() + "\", plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\")";
    }   

    /**
     * @return the filePath
     */
    public String getFilePath()
    {
        return (String)(((JTextField)(getMap().get("filePath"))).getText()).replaceAll("\\\\", "\\\\\\\\");
    }

    /**
     * @return String object name that would be printed in the python file
     */
    @Override
    public String getObjectName()
    {
        return "input" + super.toString();
    }

    /**
     * @return true
     */
    @Override
    public boolean hasOutput() 
    {
        return true;
    }

    /**
     * @return false
     */
    @Override
    public boolean hasInput() 
    {
        return false;
    }

    /**
     * @return the type of the block ("Input Block")
     */
    @Override
    public String getType() 
    {
        return "Input Block";
    }
}

class Clock extends RectangleBlock
{
    /**
     * Creates a Clock object
     * @param name : the name of the clock
     * @param rect : the Rectangle which is to be drawn
     * @param color : the color of the Rectangle
     * @param panel : the DrawCircuit upon which the Rectangle would be drawn
     */
    public Clock(String name, Rectangle rect, Color color, DrawCircuit panel)
    {
        super(name, rect, color, panel);
        LinkedHashMap<String, Component> map = new LinkedHashMap<>();
        map.put("plot", createOptions(new String [] {"True", "False"}, "False"));
        map.put("blockID", createTextField(name));
        map.put("timePeriod", createFloatField(1.2));
        map.put("onTime", createFloatField(0.6));
        map.put("initialValue", createIntField(0, 0, 1));
        map.put("Delete", createDeleteButton("Delete Clock"));
        setMap(map);
    }

    /**
     * @return String representation of the block
     */
    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.clock(plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\"" +  
            ", timePeriod = " + getTimePeriod() +", onTime = " + getOnTime() + ", initialValue = " + getInitialValue() + ")";
    }

    /**
     * @return String object name that would be printed in the python file
     */
    @Override
    public String getObjectName()
    {
        return "clock" + super.toString();
    }

    /**
     * @return String representation of the time period of the clock
     */
    public String getTimePeriod()
    {
        return (String)(((JTextField)(getMap().get("timePeriod"))).getText());
    }

    /**
     * @return String representation of the on time of the clock
     */
    public String getOnTime()
    {
        return (String)(((JTextField)(getMap().get("onTime"))).getText());
    }

    /**
     * @return the initial value of the clock
     */
    public String getInitialValue()
    {
        return ((JSpinner)(getMap().get("initialValue"))).getValue().toString();
    }

    /**
     * @return true
     */
    @Override
    public boolean hasOutput() 
    {
        return true;
    }

    /**
     * @return false
     */
    @Override
    public boolean hasInput() 
    {
        return false;
    }

    /**
     * @return the type of the object "Clock"
     */
    @Override
    public String getType() 
    {
        return "Clock";
    }
}

class Output extends RectangleBlock
{
    /**
     * Creates a new Output object
     * @param name : the name of the block
     * @param rect : the rectangle which is to be drawn
     * @param color : the color of the rectangle
     * @param panel : the DrawCircuit upon which the rectangle would be drawn
     */
    public Output(String name, Rectangle rect, Color color, DrawCircuit panel)
    {
        super(name, rect, color, panel);
        LinkedHashMap<String, Component> map = new LinkedHashMap<>();
        map.put("plot", createOptions(new String [] {"True", "False"}, "False"));
        map.put("blockID", createTextField(name));
        map.put("Delete", createDeleteButton("Delete Output Block"));
        setMap(map);
    }

    /**
     * @return String representation of the block
     */
    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.output(plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\"" + ")";
    }

    /**
     * @return String object name that would be printed in the python file
     */
    @Override
    public String getObjectName()
    {
        return "output" + super.toString();
    }

    /**
     * @return false
     */
    @Override
    public boolean hasOutput() 
    {
        return false;
    }

    /**
     * @return true
     */
    @Override
    public boolean hasInput() 
    {
        return true;
    }

    /**
     * @return type of the object "Output Block"
     */
    @Override
    public String getType() 
    {
        return "Output Block";
    }
}

class Combinational extends RectangleBlock
{
    /**
     * Creates a new combinational object
     * @param name : the name of the block
     * @param rect : the rectangle which is to be drawn
     * @param color : the color of the rectangle
     * @param panel : the DrawCircuit upon which the rectangle would be drawn
     */
    public Combinational(String name, Rectangle rect, Color color, DrawCircuit panel)
    {
        super(name, rect, color, panel);
        LinkedHashMap<String, Component> map = new LinkedHashMap<>();
        map.put("maxOutSize", createIntField(1, 0, Integer.MAX_VALUE));
        map.put("plot", createOptions(new String [] {"True", "False"}, "False"));
        map.put("blockID", createTextField(name));
        map.put("func", createTextField("lambda x: x"));
        map.put("delay", createIntField(0, 0, Integer.MAX_VALUE));
        map.put("initialValue", createIntField(0, 0, Integer.MAX_VALUE));
        map.put("Delete", createDeleteButton("Delete Combinational Block"));
        setMap(map);
    }

    /**
     * @return String representation of the block
     */
    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.combinational(maxOutSize = "+getMaxOutSize() + ", plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\"" +  
            ", func = " + getFunc() +", delay = " + getDelay() + ", initialValue = " + getInitialValue() + ")";
    }

    /**
     * @return the maximum number of output wires
     */
    public Integer getMaxOutSize()
    {
        return (Integer)(((JSpinner)(getMap().get("maxOutSize"))).getValue());
    }

    /**
     * @return String representation of the function of the combinational block
     */
    public String getFunc() 
    {
        return (String)(((JTextField)(getMap().get("func"))).getText());
    }

    /**
     * @return String representation of the delay
     */
    public String getDelay()
    {
        return ((JSpinner)(getMap().get("delay"))).getValue().toString();
    }

    /**
     * @return String representation of the initial value
     */
    public String getInitialValue()
    {
        return ((JSpinner)(getMap().get("initialValue"))).getValue().toString();
    }

    /**
     * @return String object name that would be printed in the python file
     */
    @Override
    public String getObjectName()
    {
        return "comb" + super.toString();
    }

    /**
     * @return true
     */
    @Override
    public boolean hasOutput() 
    {
        return true;
    }

    /**
     * @return true
     */
    @Override
    public boolean hasInput() 
    {
        return true;
    }

    /**
     * @return the type of the block "Combinational Block"
     */
    @Override
    public String getType() 
    {
        return "Combinational Block";
    }
}

class Wire extends Block
{
    private Block startBlock, endBlock;
    private JLabel startLabel, endLabel;
    private Polygon arrowHead;

    /**
     * Creates a new wire object
     * @param name : the name of the wire
     * @param line : the Line object which is to be drawn
     * @param color : the color of the wire
     * @param panel : the DrawCircuit on which the Wire would be drawn
     */
    public Wire(String name, Line2D.Double line, Color color, DrawCircuit panel)
    {
        super(name, line, color, panel);

        startLabel = createLabel();
        endLabel = createLabel();
        startLabel.setBackground(Color.WHITE);
        startLabel.setOpaque(true);
        endLabel.setBackground(Color.WHITE);
        endLabel.setOpaque(true);

        startLabel.setText(getStartBlock() == null ? "None" : getStartBlock().getName());
        endLabel.setText(getEndBlock() == null ? "None" : getEndBlock().getName());

        LinkedHashMap<String, Component> map = new LinkedHashMap<>();
        map.put("Wire ID", createTextField("wire"));
        map.put("Output LSB (inclusive)", createTextField("--"));
        map.put("Output MSB (exclusive)", createTextField("--"));
        map.put("Input Block (with output wires)", startLabel);
        map.put("Output Block (with input wires)", endLabel);
        map.put("Is Clock Line", createOptions(new String [] {"True", "False"}, "False"));
        map.put("Delete", createDeleteButton("Delete Wire"));
        setMap(map);

        //Creates the arrow object at the tip of the wire
        int x1 = (int)(line.x1), y1 = (int)(line.y1), x2 = (int)(line.x2), y2 = (int)(line.y2);
    
        double angle = Math.atan2(y2 - y1, x2 - x1);
        int arrowLength = 10;

        int[] arrowX = 
        {
            x2,                                            
            (int) (x2 - arrowLength * Math.cos(angle - Math.PI / 6)),
            (int) (x2 - arrowLength * Math.cos(angle + Math.PI / 6))
        };
        int[] arrowY = 
        {
            y2,                                            
            (int) (y2 - arrowLength * Math.sin(angle - Math.PI / 6)),
            (int) (y2 - arrowLength * Math.sin(angle + Math.PI / 6))
        };

        arrowHead = new Polygon(arrowX, arrowY, 3);

        panel.repaint();
    }

    /**
     * Sets the starting block/ending block of the Wire
     * @param block : the starting block/ending block
     */
    public void setBlock(Block block)
    {
        if(startBlock == null) 
        {
            startBlock = block;
        }
        else endBlock = block;
    }

    /**
     * Sets the starting block of the wire
     * @param block : the new staring block
     * @param inputWire : the input wire
     */
    public void setStartBlock(Block block, Wire inputWire)
    {
        startBlock = block;
    }

    /**
     * @return true if the wire is a clock wire
     */
    @SuppressWarnings("unchecked")
    public boolean isClocked()
    {
        if(((JComboBox<String>)(getMap().get("Is Clock Line"))).getSelectedItem().equals("True"))
            return true;
        
        return false;
    }

    /**
     * @return the starting block
     */
    public Block getStartBlock()
    {
        return startBlock;
    }

    /**
     * @return the ending block
     */
    public Block getEndBlock()
    {
        return endBlock;
    }

    /**
     * @return get the output wire's MSB
     */
    public String getOutputMSB()
    {
        try
        {
            return Integer.parseInt(((JTextField)(getMap().get("Output MSB (exclusive)"))).getText()) + "";
        }
        catch(NumberFormatException e)
        {
            return null;
        }
    }

    /**
     * @return get the output wire's LSB
     */
    public String getOutputLSB()
    {
        try
        {
            return Integer.parseInt(((JTextField)(getMap().get("Output LSB (inclusive)"))).getText()) + "";
        }
        catch(NumberFormatException e)
        {
            return null;
        }
    }

    /**
     * @return get the output String
     */
    public String getOutputString()
    {
        String outputMSB = getOutputMSB(), outputLSB = getOutputLSB();
        
        if(outputMSB == null || outputLSB == null)
            return "";
        
        return outputLSB + ":" + outputMSB;
    }

    /**
     * @return Polygon arrowhead of the end of the block
     */
    public Polygon getArrowHead()
    {
        return arrowHead;
    }

    /**
     * Updates the start label and end label
     */
    public void updateBlocks()
    {
        startLabel.setText(getStartBlock() == null ? "None" : getStartBlock().getName());
        endLabel.setText(getEndBlock() == null ? "None" : getEndBlock().getName());
    }
}