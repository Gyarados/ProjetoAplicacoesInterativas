using System.Runtime.InteropServices;

using Websocket.Client;

using WebsocketARTracking;

namespace WebsocketTest {
    class Program {
        [DllImport("user32.dll")] // import para movimentação do mouse
        static extern bool SetCursorPos(int X, int Y);

        public static void MoveCursorToPoint(int x, int y) {
            SetCursorPos(x, y);
        }

        static void Main(string[] args) {
            Program prg = new Program();
            prg.Initialize();
        }

        private void Initialize() {
            Console.CursorVisible = false;

            double S = 0.1; // sensibilidade

            double h_ref = 960; // número de pixel horizontais dividido por 2
            double h_density = 55.81395348837209; // número de pixel horizontais divido pela altura em centímetros

            double v_ref = 540; // número de pixel verticais dividido por 2
            double v_density = 55.95854922279793; // número de pixel verticais divido pela altura em centímetros

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