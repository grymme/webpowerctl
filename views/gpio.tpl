<!DOCTYPE html>
<html>
    <head>
        <meta  content="text/html; charset=UTF-8"  http-equiv="content-type">
        <title>Westermo power control</title>
       <link rel="stylesheet" href="/static/train.css">
        </head>
    <body>
        <center>
        <table class="ButtonTable">
            <tr><td> <h1>GPIO settings for power control</h1></td></tr>
        </table>
        <p><br></p>       
        % print('Template :' + str(gpio))
        <form action="/gpio" method="post">
        <table class="ButtonTable">
        <tbody>
                % x = 0
                % for button in buttons:                
                <tr>
                    <td id="tabletext">
                        <h1 id="switch_text">{{button[1]}}</h1>
                    </td>
                    <td>
                        <div class="switch">
                            <input type="checkbox" id="{{button[1]}}" name="powerbutton[{{x}}]" value="True" 
                        % print("X is " + str(x) + ", " + gpio[x])
                        % if gpio[x] == "True":
                        checked
                        % end
                        >
                    <label><i></i></label>
                    </center>
                </td>
            </tr>
               % x += 1
            % end
            <tr><td/>
                <td>
                    <input type=submit class="SubmitBtn" name="btn" value="Apply">
                </td>
            </tr>
        </tbody>
    </table>
    <br>
    <table class="ButtonTable">
        <tr><td align="center" valign="top"><h2>Status message</h2></td></tr>
        <tr><td><div class="StatusText">Result: {{result}}</div></td></tr>
        <tr><td><div class="StatusText">Status: {{status}}</div></td></tr>
    </center>
</body>
</html>

