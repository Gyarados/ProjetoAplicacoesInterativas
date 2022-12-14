// <auto-generated />
//
// To parse this JSON data, add NuGet 'Newtonsoft.Json' then do:
//
//    using WebsocketARTracking;
//
//    var welcome = Welcome.FromJson(jsonString);

namespace WebsocketARTracking
{
    using System.Globalization;
    using Newtonsoft.Json;
    using Newtonsoft.Json.Converters;

    public partial class Welcome
    {
        [JsonProperty("timestamp")]
        public double Timestamp { get; set; }

        [JsonProperty("success")]
        public bool Success { get; set; }

        [JsonProperty("translation_x")]
        public double TranslationX { get; set; }

        [JsonProperty("translation_y")]
        public double TranslationY { get; set; }

        [JsonProperty("translation_z")]
        public double TranslationZ { get; set; }

        [JsonProperty("rotation_right_x")]
        public double RotationRightX { get; set; }

        [JsonProperty("rotation_right_y")]
        public double RotationRightY { get; set; }

        [JsonProperty("rotation_right_z")]
        public double RotationRightZ { get; set; }

        [JsonProperty("rotation_up_x")]
        public double RotationUpX { get; set; }

        [JsonProperty("rotation_up_y")]
        public double RotationUpY { get; set; }

        [JsonProperty("rotation_up_z")]
        public double RotationUpZ { get; set; }

        [JsonProperty("rotation_forward_x")]
        public double RotationForwardX { get; set; }

        [JsonProperty("rotation_forward_y")]
        public double RotationForwardY { get; set; }

        [JsonProperty("rotation_forward_z")]
        public double RotationForwardZ { get; set; }
    }

    public partial class Welcome
    {
        public static Welcome FromJson(string json) => JsonConvert.DeserializeObject<Welcome>(json, WebsocketARTracking.Converter.Settings);
    }

    public static class Serialize
    {
        public static string ToJson(this Welcome self) => JsonConvert.SerializeObject(self, WebsocketARTracking.Converter.Settings);
    }

    internal static class Converter
    {
        public static readonly JsonSerializerSettings Settings = new JsonSerializerSettings
        {
            MetadataPropertyHandling = MetadataPropertyHandling.Ignore,
            DateParseHandling = DateParseHandling.None,
            Converters =
            {
                new IsoDateTimeConverter { DateTimeStyles = DateTimeStyles.AssumeUniversal }
            },
        };
    }
}