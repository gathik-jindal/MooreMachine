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

public class Block 
{
    private Rectangle rect;
    private Line2D.Double line;
    private Color color;
    private String name;
    private Map<String, Component> map;
    private DrawingPanel drawingPanel;
    private int currID = 0;
    private static int id = 0;

    public Block(String name, Rectangle rect, Color color, DrawingPanel panel) 
    {
        this.name = name;
        this.rect = rect;
        this.color = color;
        this.map = new LinkedHashMap<>();
        this.drawingPanel = panel;
        this.currID = id;

        id++;
    }

    public Block(String name, Line2D.Double line, Color color, DrawingPanel panel)
    {
        this.name = name;
        this.line = line;
        this.color = color;
        this.map = new LinkedHashMap<>();
        this.drawingPanel = panel;
        this.currID = id;

        id++;
    }

    public void setRect(Rectangle rect, Color color) 
    {
        this.rect = rect;
        this.color = color;
    }

    public void setLine(Line2D.Double line, Color color)
    {
        this.line = line;
        this.color = color;
    }

    public Rectangle getRect() 
    {
        return this.rect;
    }

    public Line2D.Double getLine()
    {
        return this.line;
    }

    public Color getColor() 
    {
        return this.color;
    }

    public String getName() 
    {
        if(map.containsKey("blockID"))
            return ((JTextField)(map.get("blockID"))).getText();
        
        return this.name;
    }

    public Map<String, Component> getMap()
    {
        return this.map;
    }

    public void setMap(Map<String, Component> fields)
    {
        this.map = fields;
    }

    private void applyFormatting(Component component)
    {
        component.setFont(new Font("Arial", Font.PLAIN, 12));
        component.setPreferredSize(new Dimension(200, 25));
        component.setMaximumSize(new Dimension(200, 25));
        component.setBackground(Color.WHITE);
    }

    protected JTextField createTextField(String value)
    {
        JTextField jTextField = new JTextField(value);
        
        applyFormatting(jTextField);
        jTextField.setEditable(true);
        jTextField.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        
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

    protected JLabel createLabel()
    {
        JLabel label = new JLabel();
        applyFormatting(label);
        label.setBorder(BorderFactory.createLineBorder(Color.GRAY));

        return label;
    }

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

    @Override
    public String toString()
    {
        return currID + "";
    }

    @SuppressWarnings("unchecked")
    public String getPlot()
    {
        return (String)(((JComboBox<String>)(map.get("plot"))).getSelectedItem());
    }

    public String getBlockID()
    {
        return (String)(((JTextField)(map.get("blockID"))).getText());
    }
}

abstract class RectangleBlock extends Block
{
    public RectangleBlock(String name, Rectangle rect, Color color, DrawingPanel panel)
    {
        super(name, rect, color, panel);
    }

    public String getObjectName()
    {
        return "rectangle_block" + super.toString();
    }

    public abstract boolean hasOutput();
    public abstract boolean hasInput();
    public abstract String getType();
}

class Moore extends RectangleBlock
{
    public Moore(String name, Rectangle rect, Color color, DrawingPanel panel)
    {
        super(name, rect, color, panel);
        LinkedHashMap<String, Component> map = new LinkedHashMap<>();
        map.put("maxOutSize", createIntField(1, 0, Integer.MAX_VALUE));
        map.put("plot", createOptions(new String [] {"True", "False"}, "False"));
        map.put("blockID", createTextField(name));
        map.put("nsl", createTextField("lambda ps, i: 0"));
        map.put("ol", createTextField("lambda ps, i: 0"));
        map.put("startingState", createIntField(0, 0, Integer.MAX_VALUE));
        map.put("Delete", createDeleteButton("Delete Moore Machine"));
        setMap(map);
    }

    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.moore(maxOutSize = "+getMaxOutSize() + ", plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\"" +  
            ", nsl = " + getNSL() +", ol = " + getOL() + ", startingState = " + getStartingState() + ")";
    }

    public Integer getMaxOutSize()
    {
        return (Integer)(((JSpinner)(getMap().get("maxOutSize"))).getValue());
    }

    public String getNSL()
    {
        return (String)(((JTextField)(getMap().get("nsl"))).getText());
    }

    public String getOL()
    {
        return (String)(((JTextField)(getMap().get("ol"))).getText());
    }

    public Integer getStartingState()
    {
        return (Integer)(((JSpinner)(getMap().get("startingState"))).getValue());
    }

    @Override
    public String getObjectName()
    {
        return "moore" + super.toString();
    }

    @Override
    public boolean hasOutput() 
    {
        return true;
    }

    @Override
    public boolean hasInput() 
    {
        return true;
    }

    @Override
    public String getType() 
    {
        return "Moore";
    }
}

class Input extends RectangleBlock
{
    public Input(String name, Rectangle rect, Color color, DrawingPanel panel)
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

    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.source(filePath = \""+getFilePath() + "\", plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\")";
    }

    public String getFilePath()
    {
        return (String)(((JTextField)(getMap().get("filePath"))).getText());
    }

    @Override
    public String getObjectName()
    {
        return "input" + super.toString();
    }

    @Override
    public boolean hasOutput() 
    {
        return true;
    }

    @Override
    public boolean hasInput() 
    {
        return false;
    }

    @Override
    public String getType() 
    {
        return "Input Block";
    }
}

class Clock extends RectangleBlock
{
    public Clock(String name, Rectangle rect, Color color, DrawingPanel panel)
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

    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.clock(plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\"" +  
            ", timePeriod = " + getTimePeriod() +", onTime = " + getOnTime() + ", initialValue = " + getInitialValue() + ")";
    }

    @Override
    public String getObjectName()
    {
        return "clock" + super.toString();
    }

    public String getTimePeriod()
    {
        return (String)(((JTextField)(getMap().get("timePeriod"))).getText());
    }

    public String getOnTime()
    {
        return (String)(((JTextField)(getMap().get("onTime"))).getText());
    }

    public String getInitialValue()
    {
        return ((JSpinner)(getMap().get("initialValue"))).getValue().toString();
    }

    @Override
    public boolean hasOutput() 
    {
        return true;
    }

    @Override
    public boolean hasInput() 
    {
        return false;
    }

    @Override
    public String getType() 
    {
        return "Clock";
    }
}

class Output extends RectangleBlock
{
    public Output(String name, Rectangle rect, Color color, DrawingPanel panel)
    {
        super(name, rect, color, panel);
        LinkedHashMap<String, Component> map = new LinkedHashMap<>();
        map.put("plot", createOptions(new String [] {"True", "False"}, "False"));
        map.put("blockID", createTextField(name));
        map.put("Delete", createDeleteButton("Delete Output Block"));
        setMap(map);
    }

    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.output(plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\"" + ")";
    }

    @Override
    public String getObjectName()
    {
        return "output" + super.toString();
    }

    @Override
    public boolean hasOutput() 
    {
        return false;
    }

    @Override
    public boolean hasInput() 
    {
        return true;
    }

    @Override
    public String getType() 
    {
        return "Output Block";
    }
}

class Combinational extends RectangleBlock
{
    public Combinational(String name, Rectangle rect, Color color, DrawingPanel panel)
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

    @Override
    public String toString()
    {
        return getObjectName() + " = pysim.combinational(maxOutSize = "+getMaxOutSize() + ", plot = " + getPlot() + ", blockID = \"" + getBlockID() + "\"" +  
            ", func = " + getFunc() +", delay = " + getDelay() + ", initialValue = " + getInitialValue() + ")";
    }

    public Integer getMaxOutSize()
    {
        return (Integer)(((JSpinner)(getMap().get("maxOutSize"))).getValue());
    }

    public String getFunc()
    {
        return (String)(((JTextField)(getMap().get("func"))).getText());
    }

    public String getDelay()
    {
        return ((JSpinner)(getMap().get("delay"))).getValue().toString();
    }

    public String getInitialValue()
    {
        return ((JSpinner)(getMap().get("initialValue"))).getValue().toString();
    }

    @Override
    public String getObjectName()
    {
        return "comb" + super.toString();
    }

    @Override
    public boolean hasOutput() 
    {
        return true;
    }

    @Override
    public boolean hasInput() 
    {
        return true;
    }

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

    public Wire(String name, Line2D.Double line, Color color, DrawingPanel panel)
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

    public void setBlock(Block block)
    {
        if(startBlock == null) 
        {
            startBlock = block;

            if(block instanceof Wire)
            {
                Wire inputWire = (Wire)(block);
                getMap().put("Is Clock Line", createOptions(new String [] {"True", "False"}, isClocked(this, inputWire)));
            }
        }
        else endBlock = block;
    }

    public void setStartBlock(Block block, Wire inputWire)
    {
        startBlock = block;
        getMap().put("Is Clock Line", createOptions(new String [] {"True", "False"}, isClocked(this, inputWire)));
    }

    @SuppressWarnings("unchecked")
    private static String isClocked(Wire w1, Wire w2)
    {
        if(((JComboBox<String>)(w1.getMap().get("Is Clock Line"))).getSelectedItem().equals("True") || 
            ((JComboBox<String>)(w1.getMap().get("Is Clock Line"))).getSelectedItem().equals("True"))
            return "True";
        
            return "False";
    }

    @SuppressWarnings("unchecked")
    public boolean isClocked()
    {
        if(((JComboBox<String>)(getMap().get("Is Clock Line"))).getSelectedItem().equals("True"))
            return true;
        
        return false;
    }

    public Block getStartBlock()
    {
        return startBlock;
    }

    public Block getEndBlock()
    {
        return endBlock;
    }

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

    public String getOutputString()
    {
        String outputMSB = getOutputMSB(), outputLSB = getOutputLSB();
        
        if(outputMSB == null || outputLSB == null)
            return "";
        
        return outputLSB + ":" + outputMSB;
    }

    public Polygon getArrowHead()
    {
        return arrowHead;
    }

    public void updateBlocks()
    {
        startLabel.setText(getStartBlock() == null ? "None" : getStartBlock().getName());
        endLabel.setText(getEndBlock() == null ? "None" : getEndBlock().getName());
    }
}