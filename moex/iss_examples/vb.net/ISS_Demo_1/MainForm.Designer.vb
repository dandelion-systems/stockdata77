<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class MainForm
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.btn_get = New System.Windows.Forms.Button()
        Me.btn_auth = New System.Windows.Forms.Button()
        Me.txt_auth = New System.Windows.Forms.TextBox()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.txt_username = New System.Windows.Forms.TextBox()
        Me.Label2 = New System.Windows.Forms.Label()
        Me.txt_password = New System.Windows.Forms.TextBox()
        Me.ResultGrid = New System.Windows.Forms.DataGridView()
        Me.secid = New System.Windows.Forms.DataGridViewTextBoxColumn()
        Me.closeprice = New System.Windows.Forms.DataGridViewTextBoxColumn()
        Me.numtrades = New System.Windows.Forms.DataGridViewTextBoxColumn()
        Me.DateTimePicker1 = New System.Windows.Forms.DateTimePicker()
        Me.listbox_engine = New System.Windows.Forms.ListBox()
        Me.btn_engines = New System.Windows.Forms.Button()
        Me.listbox_market = New System.Windows.Forms.ListBox()
        Me.listbox_board = New System.Windows.Forms.ListBox()
        CType(Me.ResultGrid, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.SuspendLayout()
        '
        'btn_get
        '
        Me.btn_get.Enabled = False
        Me.btn_get.Location = New System.Drawing.Point(223, 273)
        Me.btn_get.Name = "btn_get"
        Me.btn_get.Size = New System.Drawing.Size(149, 23)
        Me.btn_get.TabIndex = 1
        Me.btn_get.Text = "Get data"
        Me.btn_get.UseVisualStyleBackColor = True
        '
        'btn_auth
        '
        Me.btn_auth.Location = New System.Drawing.Point(11, 72)
        Me.btn_auth.Name = "btn_auth"
        Me.btn_auth.Size = New System.Drawing.Size(75, 23)
        Me.btn_auth.TabIndex = 3
        Me.btn_auth.Text = "Authenticate"
        Me.btn_auth.UseVisualStyleBackColor = True
        '
        'txt_auth
        '
        Me.txt_auth.AcceptsReturn = True
        Me.txt_auth.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Left) _
            Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.txt_auth.Location = New System.Drawing.Point(233, 11)
        Me.txt_auth.Multiline = True
        Me.txt_auth.Name = "txt_auth"
        Me.txt_auth.ReadOnly = True
        Me.txt_auth.ScrollBars = System.Windows.Forms.ScrollBars.Both
        Me.txt_auth.Size = New System.Drawing.Size(578, 84)
        Me.txt_auth.TabIndex = 4
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(13, 15)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(58, 13)
        Me.Label1.TabIndex = 5
        Me.Label1.Text = "Username:"
        '
        'txt_username
        '
        Me.txt_username.Location = New System.Drawing.Point(77, 11)
        Me.txt_username.Name = "txt_username"
        Me.txt_username.Size = New System.Drawing.Size(149, 20)
        Me.txt_username.TabIndex = 6
        '
        'Label2
        '
        Me.Label2.AutoSize = True
        Me.Label2.Location = New System.Drawing.Point(15, 49)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(56, 13)
        Me.Label2.TabIndex = 7
        Me.Label2.Text = "Password:"
        '
        'txt_password
        '
        Me.txt_password.Location = New System.Drawing.Point(77, 46)
        Me.txt_password.Name = "txt_password"
        Me.txt_password.Size = New System.Drawing.Size(150, 20)
        Me.txt_password.TabIndex = 8
        Me.txt_password.UseSystemPasswordChar = True
        '
        'ResultGrid
        '
        Me.ResultGrid.Anchor = CType((((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) _
            Or System.Windows.Forms.AnchorStyles.Left) _
            Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.ResultGrid.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
        Me.ResultGrid.Columns.AddRange(New System.Windows.Forms.DataGridViewColumn() {Me.secid, Me.closeprice, Me.numtrades})
        Me.ResultGrid.Location = New System.Drawing.Point(12, 306)
        Me.ResultGrid.Name = "ResultGrid"
        Me.ResultGrid.Size = New System.Drawing.Size(799, 426)
        Me.ResultGrid.TabIndex = 9
        '
        'secid
        '
        Me.secid.HeaderText = "SECID"
        Me.secid.Name = "secid"
        Me.secid.ReadOnly = True
        '
        'closeprice
        '
        Me.closeprice.HeaderText = "CLOSE"
        Me.closeprice.Name = "closeprice"
        Me.closeprice.ReadOnly = True
        '
        'numtrades
        '
        Me.numtrades.HeaderText = "NUMTRADES"
        Me.numtrades.Name = "numtrades"
        Me.numtrades.ReadOnly = True
        '
        'DateTimePicker1
        '
        Me.DateTimePicker1.Location = New System.Drawing.Point(12, 273)
        Me.DateTimePicker1.Name = "DateTimePicker1"
        Me.DateTimePicker1.Size = New System.Drawing.Size(200, 20)
        Me.DateTimePicker1.TabIndex = 16
        '
        'listbox_engine
        '
        Me.listbox_engine.FormattingEnabled = True
        Me.listbox_engine.HorizontalScrollbar = True
        Me.listbox_engine.Location = New System.Drawing.Point(90, 113)
        Me.listbox_engine.Name = "listbox_engine"
        Me.listbox_engine.ScrollAlwaysVisible = True
        Me.listbox_engine.Size = New System.Drawing.Size(236, 147)
        Me.listbox_engine.TabIndex = 17
        '
        'btn_engines
        '
        Me.btn_engines.Location = New System.Drawing.Point(11, 113)
        Me.btn_engines.Name = "btn_engines"
        Me.btn_engines.Size = New System.Drawing.Size(75, 23)
        Me.btn_engines.TabIndex = 18
        Me.btn_engines.Text = "Get engines"
        Me.btn_engines.UseVisualStyleBackColor = True
        '
        'listbox_market
        '
        Me.listbox_market.FormattingEnabled = True
        Me.listbox_market.HorizontalScrollbar = True
        Me.listbox_market.Location = New System.Drawing.Point(337, 113)
        Me.listbox_market.Name = "listbox_market"
        Me.listbox_market.ScrollAlwaysVisible = True
        Me.listbox_market.Size = New System.Drawing.Size(236, 147)
        Me.listbox_market.TabIndex = 19
        '
        'listbox_board
        '
        Me.listbox_board.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Left) _
            Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.listbox_board.FormattingEnabled = True
        Me.listbox_board.HorizontalScrollbar = True
        Me.listbox_board.Location = New System.Drawing.Point(585, 112)
        Me.listbox_board.Name = "listbox_board"
        Me.listbox_board.ScrollAlwaysVisible = True
        Me.listbox_board.Size = New System.Drawing.Size(226, 147)
        Me.listbox_board.TabIndex = 20
        '
        'MainForm
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(823, 744)
        Me.Controls.Add(Me.listbox_board)
        Me.Controls.Add(Me.listbox_market)
        Me.Controls.Add(Me.btn_engines)
        Me.Controls.Add(Me.listbox_engine)
        Me.Controls.Add(Me.DateTimePicker1)
        Me.Controls.Add(Me.ResultGrid)
        Me.Controls.Add(Me.txt_password)
        Me.Controls.Add(Me.Label2)
        Me.Controls.Add(Me.txt_username)
        Me.Controls.Add(Me.Label1)
        Me.Controls.Add(Me.txt_auth)
        Me.Controls.Add(Me.btn_auth)
        Me.Controls.Add(Me.btn_get)
        Me.Name = "MainForm"
        Me.Text = "ISS Demo v.1.2"
        CType(Me.ResultGrid, System.ComponentModel.ISupportInitialize).EndInit()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents btn_get As System.Windows.Forms.Button
    Friend WithEvents btn_auth As System.Windows.Forms.Button
    Friend WithEvents txt_auth As System.Windows.Forms.TextBox
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents txt_username As System.Windows.Forms.TextBox
    Friend WithEvents Label2 As System.Windows.Forms.Label
    Friend WithEvents txt_password As System.Windows.Forms.TextBox
    Friend WithEvents ResultGrid As System.Windows.Forms.DataGridView
    Friend WithEvents secid As System.Windows.Forms.DataGridViewTextBoxColumn
    Friend WithEvents closeprice As System.Windows.Forms.DataGridViewTextBoxColumn
    Friend WithEvents numtrades As System.Windows.Forms.DataGridViewTextBoxColumn
    Friend WithEvents DateTimePicker1 As System.Windows.Forms.DateTimePicker
    Friend WithEvents listbox_engine As System.Windows.Forms.ListBox
    Friend WithEvents btn_engines As System.Windows.Forms.Button
    Friend WithEvents listbox_market As System.Windows.Forms.ListBox
    Friend WithEvents listbox_board As System.Windows.Forms.ListBox

End Class
