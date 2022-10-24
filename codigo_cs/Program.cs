// using System;
// using System.Collections.Concurrent;
// using System.Collections.Generic;
// using System.Linq;
// using System.Text;
// using System.Threading;
// using System.Threading.Tasks;
// using System.Net.WebSockets;

using System.Runtime.InteropServices;

using Websocket.Client;

using WebsocketARTracking;

namespace WebsocketTest {
    class Program {
        // private string streaming_API_Key = "streaming_api_key";
        [DllImport("user32.dll")]
        static extern bool SetCursorPos(int X, int Y);

        public static void MoveCursorToPoint(int x, int y)
                        {
                            SetCursorPos(x, y);
                        }

        static void Main(string[] args) {
            Program prg = new Program();
            prg.Initialize();
        }

        private void Initialize() {
            Console.CursorVisible = false;

            double S = 0.1;

            double h_ref = 960;
            double h_density = 55.81395348837209;

            double v_ref = 540;
            double v_density = 55.95854922279793;

            try {
                var exitEvent = new ManualResetEvent(false);
                var url = new Uri("ws://localhost:5678");
                

                using (var client = new WebsocketClient(url)) {
                    client.ReconnectTimeout = TimeSpan.FromSeconds(30);

                    client.ReconnectionHappened.Subscribe(info =>
                    {
                        Console.WriteLine("Reconnection happened, type: " + info.Type);
                    });

                    client.MessageReceived.Subscribe(msg =>
                    {
                        Console.WriteLine("Message received: " + msg);
                        var coord = Welcome.FromJson(msg.ToString());



                        double delta_x = Math.Tan(coord.RotationRightZ * Math.PI) * coord.TranslationZ;
                        double delta_y = Math.Tan(coord.RotationUpZ * Math.PI) * coord.TranslationZ;

                        double new_coord_x = h_ref - (coord.TranslationX + S * delta_x) * h_density;
                        double new_coord_y = v_ref + (coord.TranslationY - S * delta_y) * v_density;

                        
                        Console.WriteLine("Ponto calculado: " + new_coord_x.ToString() + ", " + new_coord_y.ToString());

                        MoveCursorToPoint(((int)new_coord_x), ((int)new_coord_y));


                        // if (msg.ToString().ToLower() == "connected")
                        // {
                        //     string data = "{\"userKey\":\"" + streaming_API_Key + "\", \"symbol\":\"EURUSD,GBPUSD,USDJPY\"}";
                        //     client.Send(data);
                        // }
                    });

                    client.Start();

                    //Task.Run(() => client.Send("{ message }"));

                    exitEvent.WaitOne();
                }
            }

            catch (Exception ex) {
                Console.WriteLine("ERROR: " + ex.ToString());
            }

            Console.ReadKey();
        }

    }
}